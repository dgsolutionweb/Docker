document.addEventListener('DOMContentLoaded', function() {
    // Ativar tooltips do Bootstrap
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Funções para o formulário de movimentação
    const tipoSelect = document.getElementById('tipo');
    const quantidadeInput = document.getElementById('quantidade');
    
    if (tipoSelect && quantidadeInput) {
        tipoSelect.addEventListener('change', function() {
            if (this.value === 'saida') {
                quantidadeInput.setAttribute('max', document.querySelector('.badge').textContent.trim());
            } else {
                quantidadeInput.removeAttribute('max');
            }
        });
    }
    
    // Confirmação antes de excluir
    const deleteButtons = document.querySelectorAll('.btn-danger[data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm(this.getAttribute('data-confirm'))) {
                e.preventDefault();
            }
        });
    });
    
    // Atualização automática de formulários
    const filterForms = document.querySelectorAll('form[data-auto-submit]');
    filterForms.forEach(form => {
        const inputs = form.querySelectorAll('select, input:not([type="submit"])');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                form.submit();
            });
        });
    });
}); 