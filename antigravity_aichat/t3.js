
        window.MathJax = {
            tex: { inlineMath: [['$', '$'], ['\\(', '\\)']], displayMath: [['$$', '$$'], ['\\[', '\\]']] },
            svg: { fontCache: 'global' },
            startup: { ready() { MathJax.startup.defaultReady(); } }
        };
    