'use strict';

var API_HOST = window.location.protocol + '//' + window.location.host;

angular.module('gwt', ['gwt.site', 'angular-loading-bar'])
.constant('API_HOST', API_HOST)
.config(['cfpLoadingBarProvider', function (cfpLoadingBarProvider) {
    cfpLoadingBarProvider.includeSpinner = false;
}]);
