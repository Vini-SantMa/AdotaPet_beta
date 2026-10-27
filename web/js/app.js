import "./components.js";

const VISITOR_ID = "demo";
const $ = (selector) => document.querySelector(selector);
const state = { favoriteIds: new Set(), visiblePets: [] };

const labels = {
  species: { dog: "Cão", cat: "Gato" },
  size: { small: "Porte pequeno", medium: "Porte médio", large: "Porte grande" },
  energy: { low: "tranquila", medium: "moderada", high: "alta" },
};

async function request(url, options = {}) {
  const response = await fetch(url, options);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.detail || `Erro ${response.status} ao consultar o serviço.`);
  return payload;
}

function ageLabel(years) {
  if (years < 1) return "Filhote";
  if (years < 3) return `${years} ${years === 1 ? "ano" : "anos"} · jovem`;
  if (years < 8) return `${years} anos · adulto`;
  return `${years} anos · sênior`;
}

function makeCard(item, isRecommendation = false) {
  const pet = item.pet || item;
  const card = document.createElement("pet-card");
  const values = {
    "pet-id": pet.id,
    name: pet.name,
    "species-label": labels.species[pet.species] || "Pet",
    "age-label": ageLabel(pet.age_years),
    "size-label": labels.size[pet.size] || pet.size,
    "energy-label": labels.energy[pet.energy_level] || pet.energy_level,
    temperament: pet.temperament,
    "image-url": pet.image_url,
    favorite: state.favoriteIds.has(Number(pet.id)),
  };
  if (isRecommendation) {
    values.score = item.score;
    values["score-label"] = item.label;
    values.reasons = (item.reasons || []).join(" ");
  }
  for (const [key, value] of Object.entries(values)) card.setAttribute(key, String(value ?? ""));
  return card;
}

function renderCards(container, items, isRecommendation = false) {
  container.replaceChildren();
  if (!items.length) {
    const message = document.createElement("p");
    message.className = "empty-state";
    message.textContent = isRecommendation
      ? "Ainda não encontramos pets para mostrar. Tente deixar alguma preferência em aberto."
      : "Nenhum pet apareceu com esses filtros. Experimente mudar uma opção.";
    container.append(message);
    return;
  }
  for (const item of items) container.append(makeCard(item, isRecommendation));
}

async function refreshFavoriteIds() {
  const result = await request(`/api/favorites?visitor_id=${VISITOR_ID}`);
  state.favoriteIds = new Set(result.pet_ids.map(Number));
  $("#favoriteCount").textContent = String(state.favoriteIds.size);
}

async function loadCatalog() {
  const form = $("#filterForm");
  const params = new URLSearchParams();
  for (const [key, value] of new FormData(form).entries()) {
    if (value) params.set(key, value);
  }
  const suffix = params.size ? `?${params.toString()}` : "";
  try {
    await refreshFavoriteIds();
    const pets = await request(`/api/pets${suffix}`);
    state.visiblePets = pets;
    $("#petCount").textContent = `${pets.length} ${pets.length === 1 ? "pet encontrado" : "pets encontrados"}`;
    $("#catalogMessage").textContent = "";
    renderCards($("#petGrid"), pets);
  } catch (error) {
    $("#petCount").textContent = "Catálogo indisponível";
    $("#catalogMessage").textContent = error.message;
    renderCards($("#petGrid"), []);
  }
}

async function loadFavorites() {
  try {
    await refreshFavoriteIds();
    const pets = await request("/api/pets");
    const favorites = pets.filter((pet) => state.favoriteIds.has(Number(pet.id)));
    $("#favoritesMessage").hidden = favorites.length > 0;
    const favoriteGrid = $("#favoriteGrid");
    favoriteGrid.replaceChildren();
    if (favorites.length) renderCards(favoriteGrid, favorites);
  } catch (error) {
    $("#favoritesMessage").hidden = false;
    $("#favoritesMessage").textContent = `Não foi possível carregar os favoritos: ${error.message}`;
    $("#favoriteGrid").replaceChildren();
  }
}

async function updateFavorite(event) {
  const { petId, currentlyFavorite } = event.detail;
  try {
    await request(`/api/favorites/${petId}?visitor_id=${VISITOR_ID}`, {
      method: currentlyFavorite ? "DELETE" : "PUT",
    });
    await Promise.all([loadCatalog(), loadFavorites()]);
  } catch (error) {
    $("#catalogMessage").textContent = `Não foi possível salvar o favorito: ${error.message}`;
  }
}

document.addEventListener("favorite-toggle", updateFavorite);

document.addEventListener("pet-details", async (event) => {
  try {
    const pet = await request(`/api/pets/${event.detail.petId}`);
    const content = $("#dialogContent");
    content.replaceChildren();

    const image = document.createElement("img");
    image.className = "dialog-pet-image";
    image.src = pet.image_url;
    image.alt = `Retrato ilustrativo de ${pet.name}, animal fictício`;
    image.addEventListener("error", () => {
      const fallback = document.createElement("div");
      fallback.className = "pet-image-fallback dialog-image-fallback";
      fallback.setAttribute("role", "img");
      fallback.setAttribute("aria-label", `Imagem de ${pet.name} disponível no Preview Manus`);
      const initial = document.createElement("span");
      initial.textContent = pet.name.charAt(0).toUpperCase();
      const note = document.createElement("small");
      note.textContent = "imagem ilustrativa";
      fallback.append(initial, note);
      image.replaceWith(fallback);
    }, { once: true });
    const body = document.createElement("div");
    body.className = "dialog-pet-content";
    const kind = document.createElement("p");
    kind.className = "eyebrow";
    kind.textContent = `${labels.species[pet.species]} · perfil de demonstração`;
    const title = document.createElement("h2");
    title.id = "dialogName";
    title.textContent = pet.name;
    const story = document.createElement("p");
    story.textContent = pet.story;
    const facts = document.createElement("div");
    facts.className = "dialog-facts";
    const factItems = [
      ["Idade", ageLabel(pet.age_years)],
      ["Porte", labels.size[pet.size]],
      ["Energia", labels.energy[pet.energy_level]],
      ["Jeitinho", pet.temperament],
      ["Crianças", pet.good_with_children ? "Pode conviver" : "Precisa de avaliação"],
      ["Outros pets", pet.good_with_dogs || pet.good_with_cats ? "Pode conviver com alguns" : "Precisa de avaliação"],
    ];
    for (const [label, value] of factItems) {
      const fact = document.createElement("div");
      fact.className = "dialog-fact";
      const strong = document.createElement("strong");
      strong.textContent = label;
      const span = document.createElement("span");
      span.textContent = value;
      fact.append(strong, span);
      facts.append(fact);
    }
    body.append(kind, title, story, facts);
    content.append(image, body);
    $("#petDialog").showModal();
  } catch (error) {
    $("#catalogMessage").textContent = `Não foi possível abrir os detalhes: ${error.message}`;
  }
});

$("#closeDialog").addEventListener("click", () => $("#petDialog").close());
$("#petDialog").addEventListener("click", (event) => {
  if (event.target === $("#petDialog")) $("#petDialog").close();
});

$("#filterForm").addEventListener("change", loadCatalog);
$("#clearFilters").addEventListener("click", () => {
  $("#filterForm").reset();
  loadCatalog();
});

$("#matchForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector("button[type='submit']");
  const originalText = button.textContent;
  button.disabled = true;
  button.textContent = "Procurando combinações…";
  try {
    const data = new FormData(form);
    const preferences = {
      species: data.get("species"),
      size: data.get("size"),
      activity_level: data.get("activity_level"),
      home_type: data.get("home_type"),
      has_children: data.get("has_children") === "on",
    };
    await request(`/api/preferences?visitor_id=${VISITOR_ID}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(preferences),
    });
    await refreshFavoriteIds();
    const result = await request(`/api/recommendations?visitor_id=${VISITOR_ID}`);
    renderCards($("#recommendationGrid"), result.recommendations, true);
    $("#recommendationResults").hidden = false;
    $("#recommendationResults").scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    $("#catalogMessage").textContent = `Não foi possível calcular recomendações: ${error.message}`;
    $("#explorar").scrollIntoView({ behavior: "smooth", block: "start" });
  } finally {
    button.disabled = false;
    button.textContent = originalText;
  }
});

async function loadPreferences() {
  try {
    const preferences = await request(`/api/preferences?visitor_id=${VISITOR_ID}`);
    $("#prefSpecies").value = preferences.species;
    $("#prefSize").value = preferences.size;
    $("#prefActivity").value = preferences.activity_level;
    $("#prefHome").value = preferences.home_type;
    $("#prefChildren").checked = preferences.has_children;
  } catch {
    // O formulário já tem opções padrão acessíveis se ainda não houver preferências salvas.
  }
}

async function loadServices() {
  const gatewayText = $("#gatewayStatusText");
  const grid = $("#serviceStatus");
  try {
    const data = await request("/api/status");
    gatewayText.textContent = data.gateway === "online" ? "online" : "offline";
    const gatewayDot = document.querySelector(".gateway-status .status-dot");
    gatewayDot.classList.toggle("online", data.gateway === "online");
    gatewayDot.classList.toggle("offline", data.gateway !== "online");
    grid.replaceChildren();
    for (const service of data.services) {
      const card = document.createElement("article");
      card.className = "service-card";
      const dot = document.createElement("span");
      dot.className = `status-dot ${service.status}`;
      dot.setAttribute("aria-hidden", "true");
      const name = document.createElement("strong");
      name.textContent = service.name;
      const stateText = document.createElement("span");
      stateText.className = "status-label";
      stateText.textContent = service.status === "online" ? "em execução" : "indisponível";
      const docs = document.createElement("a");
      docs.href = service.docs_url;
      docs.target = "_blank";
      docs.rel = "noreferrer";
      docs.textContent = "Abrir documentação da API";
      card.append(dot, name, stateText, docs);
      grid.append(card);
    }
  } catch {
    gatewayText.textContent = "verifique a execução";
    grid.textContent = "Não foi possível consultar o estado dos serviços.";
  }
}

async function init() {
  await Promise.all([loadCatalog(), loadFavorites(), loadPreferences(), loadServices()]);
}

init();
