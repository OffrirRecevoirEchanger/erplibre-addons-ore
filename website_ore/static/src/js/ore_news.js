odoo.define('website.ore_News', function (require) {
    "use strict";

    require('web.dom_ready');
    require('bus.BusService');
    let ajax = require('web.ajax');
    let core = require('web.core');
    let session = require('web.session');
    let Widget = require('web.Widget');
    let QWeb = core.qweb;

    // Get existing module
    let app = angular.module('OREApp');

    app.controller('NewsController', ['$scope', function ($scope) {
        $scope.$scope_main = angular.element(document.querySelector('[ng-controller="MainController"]')).scope();
        $scope._ = _;
        $scope.dct_news_info = {}
        $scope.nb_news_info = 0;
        // $scope.$scope_main.dct_news_info = {}
        // $scope.$scope_main.nb_news_info = 0;
        $scope.load_all_news = function () {
            ajax.jsonRpc("/ore/get_info/news", "call", {}).then(function (data) {
                console.debug("AJAX receive /ore/get_info/news");
                if (data.error || !_.isUndefined(data.error)) {
                    $scope.error = data.error;
                    console.error($scope.error);
                } else if (_.isEmpty(data)) {
                    $scope.error = "Empty '/ore/get_info/news' data";
                    console.error($scope.error);
                } else {
                    $scope.dct_news_info = data;
                    const arrFromObj = Object.keys(data);
                    $scope.nb_news_info = arrFromObj.length;
                    // $scope.$scope_main.dct_news_info = data;
                    // $scope.$scope_main.nb_news_info = data.length;
                    console.debug($scope.dct_news_info);
                    console.debug($scope.nb_news_info);
                }

                // Process all the angularjs watchers
                $scope.$scope_main.$digest();
                $scope.$digest();
            }).fail(function (error, ev) {
                console.error(error);
                $scope.$scope_main.check_need_login(error);
            })
        }

        $scope.load_all_news();

    }])

    let ORENews = Widget.extend({
        start: function () {
        },
    });

    return {
        ORENews: ORENews,
    };

});
