'use strict';

var gulp = require('gulp');
var plugins = require('gulp-load-plugins')();

function getTask(task) {
    return require('./gulpTasks/' + task)(gulp, plugins);
}

gulp.task('scripts', getTask('scripts'));
gulp.task('styles', getTask('styles'));
gulp.task('webserver', getTask('webserver'));

gulp.task('watch', ['scripts', 'styles'], function () {
    gulp.watch('src/js/**/*.js', ['scripts']);
    gulp.watch('src/scss/**/*.scss', ['styles']);
});

gulp.task('default', ['watch']);
