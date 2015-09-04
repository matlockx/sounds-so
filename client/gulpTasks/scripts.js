module.exports = function (gulp, plugins) {
    'use strict';

    return function () {
        gulp.src('src/js/**/*.js')
            .pipe(plugins.concat('main.js'))
            .pipe(gulp.dest('dist/js'))
            .pipe(plugins.rename({ suffix: '.min' }))
            .pipe(plugins.uglify())
            .pipe(gulp.dest('dist/js'))
            .pipe(plugins.notify({ message: 'Scripts task completed' }));
    };

};
