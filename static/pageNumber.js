
    window.onload = function() {
        const totalPages = Math.ceil(document.body.scrollHeight / window.innerHeight);
        const pageEls = document.querySelectorAll('.footer .pageNumber');
        pageEls.forEach(el => el.textContent = `1 / ${totalPages}`); // ou autre logique
    }

