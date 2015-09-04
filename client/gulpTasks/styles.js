module.exports = function (gulp, plugins) {
    'use strict';

    return function () {
        gulp.src('src/scss/**/*.scss')
            .pipe(plugins.sourcemaps.init())
            .pipe(plugins.sass({errLogToConsole: true}))
            .pipe(plugins.sourcemaps.write())
            .pipe(plugins.autoprefixer('last 2 version'))
            .pipe(gulp.dest('dist/css'))
            .pipe(plugins.rename({ suffix: '.min' }))
            .pipe(plugins.minifyCss())
            .pipe(gulp.dest('dist/css'))
            .pipe(plugins.notify({ message: 'Styles task completed' }));
    };

};
