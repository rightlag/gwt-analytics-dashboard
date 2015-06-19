'use strict';

angular.module('gwt.site',
               ['gwt', 'ngResource', 'ui.bootstrap', 'highcharts-ng'])
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
            var crawlErrors = [];
            var siteUrls = [];
            for (var i = 0; i < value.sites.length; i++) {
                crawlErrors.push(value.sites[i].urlCrawlErrorsCounts);
                siteUrls.push(value.sites[i].siteUrl);
            }
            $scope.loaded = true;
            $scope.sites = value.sites;
            $scope.chartConfig = {
                options: {
                    chart: {
                        type: 'column',
                        style: {
                            fontFamily: 'Open Sans, sans-serif'
                        }
                    },
                    tooltip: {
                        style: {
                            fontWeight: 'bold'
                        }
                    }
                },
                plotOptions: {
                    column: {
                        pointPadding: 0,
                    }
                },
                series: [{
                    name: 'crawl errors counts',
                    data: crawlErrors
                }],
                title: {
                    text: 'gwt'
                },
                xAxis: {
                    allowDecimals: false,
                    tickInterval: 1,
                    title: {
                        text: 'sites'
                    }
                },
                yAxis: {
                    title: {
                        text: 'crawl errors counts'
                    }
                }
            };
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
                $scope.sites = value.sites;
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
