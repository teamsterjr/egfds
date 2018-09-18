var gulp = require('gulp');
var concat = require('gulp-concat');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');

var jsDest = '../build/egfds/static/js/'
var jsSrc = '../egfds/static/js/'
gulp.task('dump', function () {
  console.log(gulp.src([
    jsDest + 'jquery.js',
    jsDest + 'bootstrap.js',
    jsDest + '**/*.js'
  ]))
})
// Concatenate JS Files
gulp.task('scripts', function () {
  return gulp.src('../egfds/static/js/*.js')
    .pipe(concat('main.js'))
    .pipe(gulp.dest(jsDest))
    .pipe(rename('main.min.js'))
    .pipe(uglify())
    .pipe(gulp.dest(jsDest));
});
// Default Task
gulp.task('default', ['scripts']);
