module.exports = function (gulp, plugins) {
    'use strict';

    return function () {
        gulp.src('')
            .pipe(plugins.webserver({
                livereload: true,
                open: true,
                fallback: 'index.html'
            }));
    };

};
