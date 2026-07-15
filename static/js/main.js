document.addEventListener('DOMContentLoaded', () => {
    // 1. Smooth scrolling for navigation anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Set active class on navbar items
                document.querySelectorAll('.nav-item').forEach(item => {
                    item.classList.remove('active');
                });
                if (this.classList.contains('nav-item')) {
                    this.classList.add('active');
                }
            }
        });
    });

    // 2. Light-Dark Theme Toggle
    const themeToggleBtn = document.getElementById('theme-toggle');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }

    // 3. FAQ Accordion Dynamic Max-Height Toggling
    const faqQuestions = document.querySelectorAll('.faq-question');
    faqQuestions.forEach(question => {
        question.addEventListener('click', () => {
            const item = question.parentElement;
            const answer = item.querySelector('.faq-answer');
            const isActive = item.classList.contains('active');

            // Collapse other FAQ items for a clean experience
            document.querySelectorAll('.faq-item').forEach(faqItem => {
                faqItem.classList.remove('active');
                faqItem.querySelector('.faq-answer').style.maxHeight = '0';
            });

            if (!isActive) {
                item.classList.add('active');
                answer.style.maxHeight = answer.scrollHeight + 'px';
            }
        });
    });

    // 4. Scroll Reveal Intersection Observer
    const revealElements = document.querySelectorAll('.reveal');
    const revealOptions = {
        threshold: 0.05,
        rootMargin: '0px 0px -60px 0px'
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, revealOptions);

    revealElements.forEach(element => {
        revealObserver.observe(element);
    });

    // 5. Animated Counter Stats Intersection Observer
    const counters = document.querySelectorAll('.counter');
    const counterOptions = {
        threshold: 0.1,
        rootMargin: '0px'
    };

    const countUp = (counter) => {
        const target = +counter.getAttribute('data-target');
        let count = 0;
        const duration = 2000; // 2 seconds duration
        const stepTime = Math.abs(Math.floor(duration / target));
        
        // Ensure smooth progress for large values like 1,000,000
        const increment = Math.ceil(target / (duration / 30)); 

        const updateTimer = setInterval(() => {
            count += increment;
            if (count >= target) {
                clearInterval(updateTimer);
                counter.innerText = target.toLocaleString();
            } else {
                counter.innerText = Math.floor(count).toLocaleString();
            }
        }, 30);
    };

    const counterObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                countUp(counter);
                observer.unobserve(counter);
            }
        });
    }, counterOptions);

    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
});
