document.addEventListener('DOMContentLoaded', function() {
    console.log('Script cargado');

    // Variables globales
    const maxCards = 6;
    const cardsPerLoad = 3;
    const modal = document.getElementById('detalleEquipoModal');
    const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
    const checkLista = document.querySelector('.check-lista');
    const todosSection = document.getElementById('todos-section');

    // Función para mostrar detalles del equipo en el modal
    function showEquipmentDetails(data) {
        document.getElementById('detalle-marca').textContent = data.marca || 'N/A';
        document.getElementById('detalle-modelo').textContent = data.modelo || 'N/A';
        document.getElementById('detalle-serial').textContent = data.serial || 'N/A';
        document.getElementById('detalle-tipo').textContent = data.tipo || 'N/A';
        document.getElementById('detalle-estado').textContent = data.estado || 'N/A';
        document.getElementById('detalle-ubicacion').textContent = data.ubicacion || 'N/A';
        document.getElementById('detalle-empleado').textContent = data.empleado || 'N/A';
        document.getElementById('detalle-mac_address').textContent = data.mac_address || 'N/A';
        document.getElementById('detalle-observaciones').textContent = data.observaciones || 'N/A';
        document.getElementById('detalle-fecha_fabricacion').textContent = data.fecha_fabricacion || 'N/A';
        document.getElementById('detalle-vida_util_anios').textContent = data.vida_util_anios || 'N/A';
        document.getElementById('detalle-nombre_red').textContent = data.nombre_red || 'N/A';
        document.getElementById('detalle-proveedor').textContent = data.proveedor || 'N/A';
        document.getElementById('detalle-valor_compra').textContent = data.valor_compra || 'N/A';
        document.getElementById('detalle-fecha_compra').textContent = data.fecha_compra || 'N/A';
        document.getElementById('detalle-fecha_recepcion').textContent = data.fecha_recepcion || 'N/A';
        document.getElementById('detalle-fecha_mantenimiento').textContent = data.fecha_mantenimiento || 'N/A';
        document.getElementById('detalle-size_pantalla').textContent = data.size_pantalla || 'N/A';
        document.getElementById('detalle-resolucion').textContent = data.resolucion || 'N/A';
        document.getElementById('detalle-procesador_marca').textContent = data.procesador_marca || 'N/A';
        document.getElementById('detalle-procesador_velocidad').textContent = data.procesador_velocidad || 'N/A';
        document.getElementById('detalle-procesador_generacion').textContent = data.procesador_generacion || 'N/A';
        document.getElementById('detalle-sistema_operativo').textContent = data.sistema_operativo || 'N/A';
        document.getElementById('detalle-sistema_operativo_version').textContent = data.sistema_operativo_version || 'N/A';
        document.getElementById('detalle-sistema_operativo_bits').textContent = data.sistema_operativo_bits || 'N/A';
        document.getElementById('detalle-almacenamiento_capacidad').textContent = data.almacenamiento_capacidad || 'N/A';
        document.getElementById('detalle-memoria').textContent = data.memoria || 'N/A';
        document.getElementById('detalle-impresora_tipo').textContent = data.impresora_tipo || 'N/A';
        document.getElementById('detalle-impresora_velocidad_ppm').textContent = data.impresora_velocidad_ppm || 'N/A';
        document.getElementById('detalle-impresora_color').textContent = data.impresora_color || 'N/A';
        document.getElementById('detalle-impresora_conexion').textContent = data.impresora_conexion || 'N/A';
        document.getElementById('detalle-cpu_formato_diseno').textContent = data.cpu_formato_diseno || 'N/A';
        document.getElementById('detalle-proyector_lumens').textContent = data.proyector_lumens || 'N/A';
        document.getElementById('detalle-ups_vatios').textContent = data.ups_vatios || 'N/A';
        document.getElementById('detalle-ups_fecha_bateria').textContent = data.ups_fecha_bateria || 'N/A';
        document.getElementById('detalle-scanner_velocidad').textContent = data.scanner_velocidad || 'N/A';
        document.getElementById('detalle-scanner_color').textContent = data.scanner_color || 'N/A';
        document.getElementById('detalle-pantalla_proyector_tipo').textContent = data.pantalla_proyector_tipo || 'N/A';
        document.getElementById('detalle-server_numero_procesadores').textContent = data.server_numero_procesadores || 'N/A';
        document.getElementById('detalle-licencia_tipo').textContent = data.licencia_tipo || 'N/A';
        document.getElementById('detalle-licencia_clase').textContent = data.licencia_clase || 'N/A';
        document.getElementById('detalle-mouse_tipo').textContent = data.mouse_tipo || 'N/A';
        document.getElementById('detalle-mouse_conexion').textContent = data.mouse_conexion || 'N/A';
        document.getElementById('detalle-clase_disco').textContent = data.clase_disco || 'N/A';

        const bootstrapModal = new bootstrap.Modal(modal, { backdrop: true, keyboard: true });
        bootstrapModal.show();
    }

    // Manejador de eventos para el botón de detalles
    document.querySelectorAll('.btn-details').forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.product-card');
            const data = {
                marca: card.querySelector('.product-brand').textContent,
                modelo: card.querySelector('.product-name').textContent,
                serial: card.querySelector('.product-serial').textContent,
                tipo: card.querySelector('.product-category').textContent,
                estado: card.querySelector('.product-status').textContent,
                ubicacion: card.dataset.ubicacion || 'N/A',
                empleado: card.dataset.empleado || 'N/A',
                mac_address: card.dataset.macAddress || 'N/A',
                observaciones: card.dataset.observaciones || 'N/A',
                fecha_fabricacion: card.dataset.fechaFabricacion || 'N/A',
                vida_util_anios: card.dataset.vidaUtilAnios || 'N/A',
                nombre_red: card.dataset.nombreRed || 'N/A',
                proveedor: card.dataset.proveedor || 'N/A',
                valor_compra: card.dataset.valorCompra || 'N/A',
                fecha_compra: card.dataset.fechaCompra || 'N/A',
                fecha_recepcion: card.dataset.fechaRecepcion || 'N/A',
                fecha_mantenimiento: card.dataset.fechaMantenimiento || 'N/A',
                size_pantalla: card.dataset.sizePantalla || 'N/A',
                resolucion: card.dataset.resolucion || 'N/A',
                procesador_marca: card.dataset.procesadorMarca || 'N/A',
                procesador_velocidad: card.dataset.procesadorVelocidad || 'N/A',
                procesador_generacion: card.dataset.procesadorGeneracion || 'N/A',
                sistema_operativo: card.dataset.sistemaOperativo || 'N/A',
                sistema_operativo_version: card.dataset.sistemaOperativoVersion || 'N/A',
                sistema_operativo_bits: card.dataset.sistemaOperativoBits || 'N/A',
                almacenamiento_capacidad: card.dataset.almacenamientoCapacidad || 'N/A',
                memoria: card.dataset.memoria || 'N/A',
                impresora_tipo: card.dataset.impresoraTipo || 'N/A',
                impresora_velocidad_ppm: card.dataset.impresoraVelocidadPpm || 'N/A',
                impresora_color: card.dataset.impresoraColor || 'N/A',
                impresora_conexion: card.dataset.impresoraConexion || 'N/A',
                cpu_formato_diseno: card.dataset.cpuFormatoDiseno || 'N/A',
                proyector_lumens: card.dataset.proyectorLumens || 'N/A',
                ups_vatios: card.dataset.upsVatios || 'N/A',
                ups_fecha_bateria: card.dataset.upsFechaBateria || 'N/A',
                scanner_velocidad: card.dataset.scannerVelocidad || 'N/A',
                scanner_color: card.dataset.scannerColor || 'N/A',
                pantalla_proyector_tipo: card.dataset.pantallaProyectorTipo || 'N/A',
                server_numero_procesadores: card.dataset.serverNumeroProcesadores || 'N/A',
                licencia_tipo: card.dataset.licenciaTipo || 'N/A',
                licencia_clase: card.dataset.licenciaClase || 'N/A',
                mouse_tipo: card.dataset.mouseTipo || 'N/A',
                mouse_conexion: card.dataset.mouseConexion || 'N/A',
                clase_disco: card.dataset.claseDisco || 'N/A'
            };
            showEquipmentDetails(data);
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
        const cards = grid.querySelectorAll('.product-card');
        const loadMoreBtn = section.querySelector('.load-more-btn');
        let visibleCount = parseInt(loadMoreBtn.dataset.visibleCount) || maxCards; // Forzar inicialización a maxCards si no está definido
        const isListMode = checkLista ? checkLista.checked : false;

        cards.forEach((card, index) => {
            // Restaurar display y aplicar límite de visibilidad
            card.style.display = isListMode ? 'flex' : 'block'; // Aplicar display según modo
            if (index >= visibleCount) {
                card.classList.add('hidden'); // Forzar ocultar las excedentes
            } else {
                card.classList.remove('hidden'); // Mostrar las primeras 6
            }
        });

        loadMoreBtn.style.display = visibleCount < cards.length ? 'block' : 'none';

        const noResults = grid.querySelector('.no-results');
        if (noResults) {
            noResults.style.display = cards.length === 0 ? 'block' : 'none';
        }
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
            document.querySelectorAll('.no-results').forEach(noResult => noResult.style.display = 'none');
        });
    });

    // Filtrado por búsqueda
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const activeSection = document.querySelector('div[id$="-section"]:not([style*="display: none"])');
        const cards = activeSection.querySelectorAll('.product-card');
        let visibleCount = 0;

        cards.forEach(card => {
            const brand = card.querySelector('.product-brand').textContent.toLowerCase();
            const category = card.querySelector('.product-category').textContent.toLowerCase();
            const model = card.querySelector('.product-name').textContent.toLowerCase();
            const serial = card.querySelector('.product-serial').textContent.toLowerCase();
            const matches = brand.includes(searchTerm) || model.includes(searchTerm) || serial.includes(searchTerm) || category.includes(searchTerm);
            card.style.display = matches ? (checkLista ? checkLista.checked ? 'flex' : 'block' : 'block') : 'none'; // Aplicar display según modo
            if (matches) visibleCount++;
        });

        const noResults = activeSection.querySelector('.no-results');
        noResults.style.display = visibleCount === 0 ? 'block' : 'none';

        const loadMoreBtn = activeSection.querySelector('.load-more-btn');
        loadMoreBtn.dataset.visibleCount = maxCards; // Reiniciar a 6 tras búsqueda
        updateCardVisibility(activeSection);
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
        console.log('ConfirmDelete llamado para equipoId:', equipoId); // Depuración

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
                console.log('Enviando solicitud a /equipo/borrar/' + equipoId + '/'); // Depuración
                fetch(`/equipo/borrar/${equipoId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken') // Obtener el token CSRF
                    }
                })
                .then(response => {
                    console.log('Respuesta recibida:', response); // Depuración
                    if (!response.ok) {
                        throw new Error('Respuesta no exitosa: ' + response.status);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Datos recibidos:', data); // Depuración
                    if (data.status === 'success') {
                        Swal.fire('Eliminado', data.message, 'success').then(() => {
                            console.log('Eliminando tarjeta del DOM para equipoId:', equipoId); // Depuración
                            const card = document.querySelector(`[data-equipo-id="${equipoId}"]`).closest('.product-card');
                            if (card) {
                                card.remove();
                                console.log('Tarjeta eliminada del DOM'); // Depuración
                            } else {
                                console.log('No se encontró la tarjeta para eliminar'); // Depuración
                            }
                            updateCardVisibility(document.querySelector('div[id$="-section"]:not([style*="display: none"])'));
                        });
                    } else {
                        Swal.fire('Error', data.message, 'error');
                    }
                })
                .catch(error => {
                    console.error('Error en la solicitud:', error); // Depuración
                    Swal.fire('Error', 'Ocurrió un problema al eliminar el equipo: ' + error.message, 'error');
                });
            }
        });
    };

    // Función para obtener cookie (necesaria para CSRF)
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
        console.log('CSRF Token para', name, ':', cookieValue); // Depuración
        return cookieValue;
    }
});