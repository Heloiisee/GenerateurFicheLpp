let sectionCount = 0;

        function addSection() {
            const container = document.getElementById('sections-container');
            const sectionId = sectionCount++;

            const section = document.createElement('div');
            section.className = 'section';
            section.setAttribute('data-id', sectionId);

            section.innerHTML = `
                <h3>Section ${sectionId + 1}
                    <button type="button" class="remove-section-btn" onclick="removeSection(this)">✖</button>
                </h3>

                <label>Titre de la section :</label>
                <input type="text" name="sections[${sectionId}][title]" required>

                <label>Consignes :</label>
                <textarea name="sections[${sectionId}][instructions]" rows="3" required></textarea>

                <label>Questions :</label>
                <div class="questions-container" data-section="${sectionId}">
                    <div class="question-item">
                        <input type="text" name="sections[${sectionId}][questions][]" placeholder="Question 1">
                        <button type="button" class="remove-btn" onclick="removeQuestion(this)">✖</button>
                    </div>
                </div>
                <button type="button" onclick="addQuestion(${sectionId})">+ Ajouter une question</button>


                <label>Tableau CSV (facultatif) :</label>
                <textarea name="sections[${sectionId}][table_csv]" rows="4" placeholder="Nom,Âge\nAlice,10\nBob,12"></textarea>
            `;

            container.appendChild(section);
        }

        function addQuestion(sectionId) {
            const container = document.querySelector(`.questions-container[data-section="${sectionId}"]`);
            const count = container.querySelectorAll('.question-item').length + 1;
            const div = document.createElement('div');
            div.className = 'question-item';
            div.innerHTML = `
                <input type="text" name="sections[${sectionId}][questions][]" placeholder="Question ${count}">
                <button type="button" class="remove-btn" onclick="removeQuestion(this)">✖</button>
            `;
            container.appendChild(div);
        }

        function removeQuestion(btn) {
            btn.parentElement.remove();
        }

        function removeSection(btn) {
            btn.closest('.section').remove();
        }

        // Afficher ou masquer le barème selon le modèle choisi
        const templateSelect = document.getElementById('template');
        const baremeContainer = document.getElementById('bareme-container');

        templateSelect.addEventListener('change', () => {
            const selected = templateSelect.value;
            baremeContainer.style.display = (selected === 'pdf_template_3' || selected === 'pdf_template_4') ? 'block' : 'none';
        });

        window.onload = () => {
            addSection();
            templateSelect.dispatchEvent(new Event('change'));
        };