const VisualizationLoader = (() => {
    const taskPk = document.getElementById('taskPk').value;
    const container = document.getElementById('figures-container');
    
    if (!taskPk || !container) {
        console.error('Missing required elements!');
        return;
    }

    async function load(interactive) {
        container.innerHTML = '<div class="col-12">Загрузка...</div>';
        
        try {
            const response = await fetch(`/visual/results/${taskPk}/figures/?interactive=${interactive}`);
            const data = await response.json();
            
            let html = '';
            data.visualizations.forEach(vis => {
                html += vis.type === 'interactive' 
                    ? interactiveTemplate(vis) 
                    : staticTemplate(vis);
            });
            
            container.innerHTML = html || '<div class="col-12">Нет доступных визуализаций</div>';
        } catch(error) {
            container.innerHTML = `<div class="alert alert-danger">Ошибка: ${error.message}</div>`;
        }
    }

    const interactiveTemplate = (vis) => `
    <div class="col-md-6 mb-4">
        <div class="card h-100">
        <div class="card-body" style="height: 500px; overflow: hidden;">
            ${vis.content}
        </div>
        </div>
    </div>`;

    const staticTemplate = (vis) => `
        <div class="col-md-6 mb-4">
            <div class="card">
                <img src="data:image/png;base64,${vis.content}" 
                     class="card-img-top" 
                     alt="${vis.name}">
            </div>
        </div>`;

    return { load };
})();

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('static-btn').addEventListener('click', () => 
        VisualizationLoader.load(false));
        
    document.getElementById('interactive-btn').addEventListener('click', () => 
        VisualizationLoader.load(true));
});