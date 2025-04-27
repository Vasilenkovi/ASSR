document.addEventListener('DOMContentLoaded', () => {
    const VisualizationLoader = (() => {
        const taskPk = document.getElementById('taskPk').value;
        const container = document.getElementById('figures-container');
        const labelSelect = document.getElementById('label-select');
        let allVisualizations = [];


        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('download-vis')) {
                e.preventDefault();
                const format = e.target.dataset.format;
                const cardHeader = e.target.closest('.card-header');
                const visName = cardHeader.querySelector('.card-header-text').textContent.trim();
                
                const url = `/visual/results/${taskPk}/download-vis/?vis_name=${encodeURIComponent(visName)}&format=${format}`;
                window.open(url, '_blank');
            }
        });

        async function load(interactive) {
            container.innerHTML = '<div class="col-12">Загрузка...</div>';

            labelSelect.innerHTML = '<option value="all">Все категории</option>'; 
            try {
                const response = await fetch(`/visual/results/${taskPk}/figures/?interactive=${interactive}&timestamp=${Date.now()}`);
                const data = await response.json();
                allVisualizations = data.visualizations;

                const uniqueLabels = Array.from(new Set(data.labels)).filter(Boolean);
                uniqueLabels.forEach(label => {
                    if (![...labelSelect.options].some(opt => opt.value === label)) {
                        const opt = document.createElement("option");
                        opt.value = label;
                        opt.textContent = label;
                        labelSelect.appendChild(opt);
                    }
                });
        
                labelSelect.style.display = uniqueLabels.length > 0 ? "block" : "none";
                render("all", interactive);
        
            } catch (error) {
                container.innerHTML = `<div class="alert alert-danger">Ошибка: ${error.message}</div>`;
            }
        }

        function render(selectedLabel, interactive) {
            container.innerHTML = '';
            const generalViz = allVisualizations.filter(v => !v.meta.group_type);
            const distributionViz = allVisualizations.filter(v => v.meta.group_type === "distribution");
            const filteredDistributions = selectedLabel === "all" 
            ? distributionViz 
            : distributionViz.filter(v => 
                String(v.meta.label).trim().toLowerCase() === 
                String(selectedLabel).trim().toLowerCase()
            );
    
        let html = "";

            if (generalViz.length > 0) {
                html += `
                    <div class="col-12 mb-4">
                        <h4>Основные графики</h4>
                        <div class="row">
                            ${generalViz.map(vis => 
                                vis.meta.type === 'interactive' 
                                    ? interactiveTemplate(vis) 
                                    : staticTemplate(vis)
                            ).join('')}
                        </div>
                    </div>`;
            }

            if (filteredDistributions.length > 0) {
                const grouped = groupByName(filteredDistributions);
                Object.keys(grouped).forEach(name => {
                    html += `
                        <div class="col-12 mb-4">
                            <h4>${name}</h4>
                            <div class="row">
                                ${grouped[name].map(vis => 
                                    vis.meta.type === 'interactive' 
                                        ? interactiveTemplate(vis) 
                                        : staticTemplate(vis)
                                ).join('')}
                            </div>
                        </div>`;
                });
            }

            container.innerHTML = html || '<div class="col-12">Нет данных</div>';
        }

        function groupByLabel(visualizations) {
            const grouped = {};

            visualizations.forEach(vis => {
                const label = vis.meta.label || 'Общие';

                if (!grouped[label]) {
                    grouped[label] = [];
                }
                if (!grouped[label].some(existing => existing.meta.name === vis.meta.name)) {
                    grouped[label].push(vis);
                }
            });
            return grouped;
        }

        function groupByName(visualizations) {
            const grouped = {};
            

            visualizations.forEach(vis => {
                const name = vis.meta.name;

                if (!grouped[name]) {
                    grouped[name] = [];
                }
                if (!grouped[name].some(existing => existing.meta.label === vis.meta.label)) {
                    grouped[name].push(vis);
                }
            });
            return grouped;
        }

        const interactiveTemplate = (vis) => {
            const id = `vis-${Math.random().toString(36).substr(2, 9)}`;
            
            setTimeout(() => {
                const containerEl = document.getElementById(id);
                if (!containerEl) return;
                containerEl.innerHTML = vis.content;
                
                const scripts = containerEl.querySelectorAll('script');
                scripts.forEach(oldScript => {
                    const newScript = document.createElement('script');
                    newScript.text = oldScript.innerHTML;
                    if (oldScript.type) newScript.type = oldScript.type;
                    oldScript.remove();
                    document.body.appendChild(newScript);
                });
            }, 0);

            if (vis.meta.label == null){
                vis.meta.label = ""
            }

            return `
                <div class="col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <span class="card-header-text">${vis.meta.name}_${vis.meta.label}</span>
                            <div class="dropdown">
                                <button class="btn btn-sm btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                                    Скачать
                                </button>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item download-vis" data-format="png" href="#">PNG</a></li>
                                    <li><a class="dropdown-item download-vis" data-format="svg" href="#">SVG</a></li>
                                    <li><a class="dropdown-item download-vis" data-format="pdf" href="#">PDF</a></li>
                                </ul>
                            </div>
                        </div>
                        <div class="card-body">
                            <div id="${id}"></div>
                        </div>
                    </div>
                </div>`;
        };

        const staticTemplate = (vis) => {
            if (vis.meta.label == null){
                vis.meta.label = ""
            }
            return `
                <div class="col-md-6 mb-4">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <span class="card-header-text">${vis.meta.name}_${vis.meta.label}</span>
                            <div class="dropdown">
                                <button class="btn btn-sm btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                                    Скачать
                                </button>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item download-vis" data-format="png" href="#">PNG</a></li>
                                    <li><a class="dropdown-item download-vis" data-format="svg" href="#">SVG</a></li>
                                    <li><a class="dropdown-item download-vis" data-format="pdf" href="#">PDF</a></li>
                                </ul>
                            </div>
                        </div>
                        <img src="data:image/png;base64,${vis.content}" 
                            class="card-img-top" 
                            alt="${vis.meta.name}">
                    </div>
                </div>`;
        };

        return { load, render };
    })();


    document.getElementById('static-btn').addEventListener('click', () => {
        document.getElementById('interactive-btn').classList.remove('active');
        document.getElementById('static-btn').classList.add('active');
        VisualizationLoader.load(false);
    });

    document.getElementById('interactive-btn').addEventListener('click', () => {
        document.getElementById('static-btn').classList.remove('active');
        document.getElementById('interactive-btn').classList.add('active');
        VisualizationLoader.load(true);
    });


    document.getElementById('label-select').addEventListener('change', (e) => {
        const interactive = document.getElementById('interactive-btn').classList.contains('active');
        VisualizationLoader.render(e.target.value, interactive);
    });
});