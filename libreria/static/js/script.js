document.addEventListener('DOMContentLoaded', function() {
    console.log('Script cargado');

    // Variables globales
    const maxCards = 6;
    const cardsPerLoad = 3;
    const modal = document.getElementById('detalleEquipoModal');
    const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
    const checkLista = document.querySelector('.check-lista');
    const todosSection = document.getElementById('todos-section');
    const exportBtn = document.getElementById('exportar-excel-btn');

    // Función para mostrar detalles del equipo en el modal
    function showEquipmentDetails(data) {
        // Define los campos básicos y avanzados según tu modelo
        const camposBasicos = [
            'marca', 'modelo', 'serial', 'tipo', 'estado', 'ubicacion', 'empleado', 'mac_address', 'observaciones'
        ];
        // El resto se consideran avanzados
        const camposAvanzados = Object.keys(data).filter(key => !camposBasicos.includes(key));

        let basicHTML = '';
        let advancedHTML = '';

        camposBasicos.forEach(key => {
            const value = data[key];
            if (value && value !== 'N/A') {
                basicHTML += `
                    <div class="feature-item">
                        <span class="feature-name">${key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
                        <span class="feature-value">${value}</span>
                    </div>
                `;
            }
        });

        camposAvanzados.forEach(key => {
            const value = data[key];
            if (value && value !== 'N/A') {
                advancedHTML += `
                    <div class="feature-item">
                        <span class="feature-name">${key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
                        <span class="feature-value">${value}</span>
                    </div>
                `;
            }
        });

        document.getElementById('modal-features-basic').innerHTML = basicHTML || '<div class="text-muted">Sin información básica.</div>';
        document.getElementById('modal-features-advanced').innerHTML = advancedHTML || '<div class="text-muted">Sin detalles avanzados.</div>';

        // Mostrar el modal Bootstrap
        const modal = new bootstrap.Modal(document.getElementById('detalleEquipoModal'));
        modal.show();
    }

    // Manejador de eventos para el botón de detalles
    document.querySelectorAll('.btn-details').forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.product-card');
            const equipoId = card.dataset.equipoId; // Obtener el ID del equipo
            const csrftoken = getCookie('csrftoken');

            // Realizar solicitud AJAX para obtener los detalles del equipo
            fetch(`/equipos/detalles/${equipoId}/`, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Accept': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error al obtener los detalles del equipo: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Datos recibidos:', data); // Depuración
                showEquipmentDetails(data);
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire('Error', 'No se pudieron cargar los detalles del equipo.', 'error');
            });
        });
    });

    // Función para obtener cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Función para manejar la visibilidad de tarjetas respetando el modo y el límite inicial
    function updateCardVisibility(section) {
        const grid = section.querySelector('.products-grid');
        const cards = Array.from(grid.querySelectorAll('.product-card')).filter(card => card.style.display !== 'none');
        const loadMoreBtn = section.querySelector('.load-more-btn');
        let visibleCount = parseInt(loadMoreBtn.dataset.visibleCount) || maxCards;
        const isListMode = checkLista ? checkLista.checked : false;

        Array.from(grid.querySelectorAll('.product-card')).forEach(card => {
            if (card.style.display !== 'none') {
                card.style.display = isListMode ? 'flex' : 'block';
            }
        });

        cards.forEach((card, index) => {
            if (index >= visibleCount) {
                card.classList.add('hidden');
            } else {
                card.classList.remove('hidden');
            }
        });

        loadMoreBtn.style.display = visibleCount < cards.length ? 'block' : 'none';
        // No tocar el mensaje .no-results aquí
    }

    // Inicializar visibilidad para todas las secciones, asegurando que todos-section sea visible
    todosSection.style.display = 'block'; // Asegurar que todos-section esté visible al inicio
    document.querySelectorAll('div[id$="-section"]').forEach(section => {
        if (section !== todosSection) {
            section.style.display = 'none'; // Ocultar otras secciones inicialmente
        }
        const loadMoreBtn = section.querySelector('.load-more-btn');
        if (loadMoreBtn) {
            loadMoreBtn.dataset.visibleCount = maxCards; // Establecer explícitamente visibleCount a 6 al inicio
        }
        updateCardVisibility(section);
    });

    // Manejar el botón "Cargar más"
    document.querySelectorAll('.load-more-btn').forEach(button => {
        button.addEventListener('click', function() {
            const section = this.closest('div[id$="-section"]');
            const loadMoreBtn = section.querySelector('.load-more-btn');
            let visibleCount = parseInt(loadMoreBtn.dataset.visibleCount) || maxCards;
            visibleCount += cardsPerLoad;
            loadMoreBtn.dataset.visibleCount = visibleCount;
            updateCardVisibility(section);
        });
    });

    // Manejar el cambio de categoría
    const filterButtons = document.querySelectorAll('.filter-btn');
    const sections = document.querySelectorAll('div[id$="-section"]');
    const searchInput = document.getElementById('search-input');

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            sections.forEach(section => {
                section.style.display = section.id === `${category}-section` ? 'block' : 'none';
                if (section.style.display === 'block') {
                    const loadMoreBtn = section.querySelector('.load-more-btn');
                    loadMoreBtn.dataset.visibleCount = maxCards; // Reiniciar a 6 al cambiar categoría
                    updateCardVisibility(section);
                }
            });

            searchInput.value = '';
            document.querySelectorAll('.product-card').forEach(card => {
                card.classList.remove('hidden');
                card.style.display = checkLista ? checkLista.checked ? 'flex' : 'block' : 'block'; // Restaurar display según modo
            });
            const activeSection = document.getElementById(`${category}-section`);
            const cards = activeSection.querySelectorAll('.product-card');
            const noResults = activeSection.querySelector('.no-results');
            if (noResults) {
                noResults.style.display = cards.length === 0 ? 'block' : 'none';
            }
            exportBtn.setAttribute('data-category', this.getAttribute('data-category'));
        });
    });

    // Filtrado por búsqueda
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const activeSection = document.querySelector('div[id$="-section"]:not([style*="display: none"])');
        const cards = activeSection.querySelectorAll('.product-card');
        let visibleCount = 0;

        // Filtra y cuenta las visibles
        cards.forEach(card => {
            const brand = card.querySelector('.product-brand')?.textContent.trim().toLowerCase() || '';
            const category = card.querySelector('.product-category')?.textContent.trim().toLowerCase() || '';
            const model = card.querySelector('.product-name')?.textContent.trim().toLowerCase() || '';
            const serial = card.querySelector('.product-serial')?.textContent.trim().toLowerCase() || '';
            const matches = brand.includes(searchTerm) || model.includes(searchTerm) || serial.includes(searchTerm) || category.includes(searchTerm);

            card.style.display = matches ? (checkLista ? checkLista.checked ? 'flex' : 'block' : 'block') : 'none';
            if (matches) visibleCount++;
        });

        // Mostrar/ocultar mensaje de no resultados según las cards visibles
        const noResults = activeSection.querySelector('.no-results');
        if (noResults) {
            // Solo cuenta las cards realmente visibles (no display:none)
            const visibleCards = Array.from(cards).filter(card => card.style.display !== 'none');
            if (visibleCards.length === 0) {
                if (searchTerm) {
                    noResults.querySelector('h3').textContent = 'No hay coincidencias';
                    noResults.querySelector('p').textContent = 'No se encontraron resultados para tu búsqueda.';
                } else {
                    noResults.querySelector('h3').textContent = noResults.dataset.defaultTitle || noResults.querySelector('h3').textContent;
                    noResults.querySelector('p').textContent = noResults.dataset.defaultText || noResults.querySelector('p').textContent;
                }
                noResults.style.display = 'block';
            } else {
                noResults.style.display = 'none';
            }
        }

        const loadMoreBtn = activeSection.querySelector('.load-more-btn');
        if (loadMoreBtn) {
            loadMoreBtn.dataset.visibleCount = maxCards;
            updateCardVisibility(activeSection);
        }
    });

    // Activar/desactivar modo lista con checkbox
    if (checkLista) {
        checkLista.addEventListener('change', function() {
            const isListMode = this.checked;
            const cards = document.querySelectorAll('.product-card');
            if (cards.length > 0) {
                cards.forEach(card => {
                    card.style.display = isListMode ? 'flex' : 'block';
                });
                document.querySelectorAll('div[id$="-section"]').forEach(section => {
                    updateCardVisibility(section);
                });
            }
        });
    }

    window.confirmDelete = function(event, equipoId) {
        event.preventDefault(); // Prevenir cualquier comportamiento predeterminado
        Swal.fire({
            title: '¿Estás seguro?',
            text: '¡Esta acción eliminará el equipo permanentemente!',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                fetch(`/equipo/borrar/${equipoId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Respuesta no exitosa: ' + response.status);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.status === 'success') {
                        Swal.fire('Eliminado', data.message, 'success').then(() => {
                            const card = document.querySelector(`[data-equipo-id="${equipoId}"]`).closest('.product-card');
                            if (card) {
                                card.remove();
                            }
                            updateCardVisibility(document.querySelector('div[id$="-section"]:not([style*="display: none"])'));
                        });
                    } else {
                        Swal.fire('Error', data.message, 'error');
                    }
                })
                .catch(error => {
                    Swal.fire('Error', 'Ocurrió un problema al eliminar el equipo: ' + error.message, 'error');
                });
            }
        });
    };

    exportBtn.addEventListener('click', function(e) {
        e.preventDefault();
        const categoria = exportBtn.getAttribute('data-category');
        window.location.href = `/equipos/exportar-excel/?categoria=${categoria}`;
    });

    // Script para el formulario de asignar equipo
    const form = document.getElementById('form-asignar');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            fetch("{% url 'asignar_equipo_ajax' %}", {
                method: 'POST',
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                Swal.fire({
                    icon: data.status === 'success' ? 'success' : 'error',
                    title: data.message
                });
                if (data.status === 'success') {
                    setTimeout(() => window.location.reload(), 1500);
                }
            })
            .catch(() => {
                Swal.fire('Error', 'Ocurrió un error al asignar el equipo.', 'error');
            });
        });
    }
});