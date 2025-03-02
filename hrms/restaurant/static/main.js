document.addEventListener('DOMContentLoaded', function () {
    const navLinks = document.querySelectorAll('#nav a');
    const pages = document.querySelectorAll('.page');
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('#nav ul');

    // Mostra la prima pagina all'avvio
    pages[0].style.display = 'block';

    // Gestione dei click sui link della navbar
    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault(); // Previeni il comportamento predefinito del link

            // Nascondi tutte le pagine
            pages.forEach(page => {
                page.style.display = 'none';
            });

            // Mostra la pagina corrispondente al link cliccato
            const target = this.getAttribute('data-target');
            document.getElementById(target).style.display = 'block';

            // Rimuovi la classe 'active' da tutti i link
            navLinks.forEach(link => {
                link.classList.remove('active');
            });

            // Aggiungi la classe 'active' al link cliccato
            this.classList.add('active');
        });
    });

    // Gestione del menu hamburger
    hamburger.addEventListener('click', function () {
        navMenu.classList.toggle('active'); // Apri/chiudi il menu
    });

    // Chiudi il menu quando si clicca su un link
    navMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function () {
            navMenu.classList.remove('active');
        });
    });
});