function escapeHTML(value = "") {
  return String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[char]);
}

class MatchScore extends HTMLElement {
  connectedCallback() {
    const score = escapeHTML(this.getAttribute("score") || "0");
    const label = escapeHTML(this.getAttribute("label") || "Compatibilidade");
    const reasons = escapeHTML(this.getAttribute("reasons") || "");
    this.innerHTML = `
      <div class="match-score-inner">
        <div class="match-score-top">
          <span class="match-score-value">${score}% combina</span>
          <span class="match-score-label">${label}</span>
        </div>
        ${reasons ? `<p class="match-reasons">${reasons}</p>` : ""}
      </div>`;
  }
}

class PetCard extends HTMLElement {
  connectedCallback() {
    this.render();
  }

  render() {
    const petId = escapeHTML(this.getAttribute("pet-id") || "");
    const name = escapeHTML(this.getAttribute("name") || "Pet");
    const species = escapeHTML(this.getAttribute("species-label") || "Pet");
    const age = escapeHTML(this.getAttribute("age-label") || "Idade não informada");
    const size = escapeHTML(this.getAttribute("size-label") || "Porte não informado");
    const energy = escapeHTML(this.getAttribute("energy-label") || "Energia não informada");
    const temperament = escapeHTML(this.getAttribute("temperament") || "");
    const image = escapeHTML(this.getAttribute("image-url") || "");
    const favorite = this.getAttribute("favorite") === "true";
    const score = this.getAttribute("score");
    const scoreLabel = this.getAttribute("score-label") || "";
    const reasons = this.getAttribute("reasons") || "";

    this.innerHTML = `
      <article class="pet-card-shell">
        <div class="pet-image-wrap">
          <img class="pet-image" src="${image}" alt="Retrato ilustrativo de ${name}, pet fictício do protótipo" loading="lazy">
          <span class="pet-kind">${species}</span>
          <button class="favorite-toggle" type="button" aria-label="${favorite ? "Remover" : "Adicionar"} ${name} ${favorite ? "dos" : "aos"} favoritos" aria-pressed="${favorite}">${favorite ? "♥" : "♡"}</button>
        </div>
        <div class="pet-card-body">
          <div class="pet-title-row"><h3 class="pet-title">${name}</h3><span class="pet-age">${age}</span></div>
          <p class="pet-temperament">${temperament}</p>
          <div class="pet-traits"><span class="trait-chip">${size}</span><span class="trait-chip">Energia ${energy}</span></div>
          ${score !== null ? `<match-score score="${escapeHTML(score)}" label="${escapeHTML(scoreLabel)}" reasons="${escapeHTML(reasons)}"></match-score>` : ""}
          <div class="card-bottom"><span class="trait-chip">Perfil de demonstração</span><button class="details-button" type="button">Conhecer ${name} <span aria-hidden="true">→</span></button></div>
        </div>
      </article>`;

    const petImage = this.querySelector(".pet-image");
    petImage.addEventListener("error", () => {
      const fallback = document.createElement("div");
      fallback.className = "pet-image-fallback";
      fallback.setAttribute("role", "img");
      fallback.setAttribute("aria-label", `Imagem de ${name} disponível no Preview Manus`);
      const initial = document.createElement("span");
      initial.textContent = name.charAt(0).toUpperCase();
      const note = document.createElement("small");
      note.textContent = "imagem ilustrativa";
      fallback.append(initial, note);
      petImage.replaceWith(fallback);
    }, { once: true });

    this.querySelector(".favorite-toggle").addEventListener("click", () => {
      this.dispatchEvent(new CustomEvent("favorite-toggle", {
        bubbles: true,
        composed: true,
        detail: { petId: Number(petId), currentlyFavorite: favorite },
      }));
    });
    this.querySelector(".details-button").addEventListener("click", () => {
      this.dispatchEvent(new CustomEvent("pet-details", {
        bubbles: true,
        composed: true,
        detail: { petId: Number(petId) },
      }));
    });
  }
}

if (!customElements.get("match-score")) customElements.define("match-score", MatchScore);
if (!customElements.get("pet-card")) customElements.define("pet-card", PetCard);
