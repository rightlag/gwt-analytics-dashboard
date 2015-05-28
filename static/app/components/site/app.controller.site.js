'use strict';

angular.module('gwt.site', ['gwt', 'ngResource', 'ui.bootstrap'])
.factory('Site', ['$resource', 'API_HOST', function ($resource, API_HOST) {
    return $resource(
        API_HOST + '/sites',
        { },
        { 'query': { method: 'GET', isArray: false } }
    );
}])
.controller('SiteCtrl', ['$scope', '$modal', '$window', 'Site',
                         function ($scope, $modal, $window, Site) {
    $scope.predicate = '-urlCrawlErrorsCounts';
    var sites = Site.query(
        function (value, responseHeaders) {
            $scope.sites = value.sites;
        },
        function (httpResponse) {
            if (httpResponse.status === 400) {
                $window.location.href = httpResponse.data.redirect;
            }
        }
    );

    $scope.open = function ($event, site) {
        $event.preventDefault();
        $modal.open({
            templateUrl: 'errors.html',
            controller: 'ModalErrorCtrl',
            size: 'lg',
            resolve: {
                site: function () {
                    return site;
                }
            }
        });
    };

    $scope.query = function () {
        $scope.error = false;
        var query = new Site($scope.url);
        query.$save(
            function (value, responseHeaders) {
                console.log(value);
            },
            function (httpResponse) {
                $scope.error = httpResponse.data.message;
            }
        );
    };
}])
.controller('ModalErrorCtrl', ['$scope', '$modalInstance', 'site',
                               function ($scope, $modalInstance, site) {
    $scope.title = 'Crawl Errors: ' + site.siteUrl;
    $scope.errors = site.urlCrawlErrorsSamples;
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);
