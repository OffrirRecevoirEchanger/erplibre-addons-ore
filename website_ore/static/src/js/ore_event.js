odoo.define('website.ore_Event', function (require) {
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

    app.controller('EventController', ['$scope', function ($scope) {
        $scope.$scope_main = angular.element(document.querySelector('[ng-controller="MainController"]')).scope();
        $scope._ = _;
        $scope.dct_event_info = {}
        $scope.nb_event_info = 0;
        // $scope.$scope_main.dct_event_info = {}
        // $scope.$scope_main.nb_event_info = 0;

        $scope.load_all_events = function () {
            ajax.jsonRpc("/ore/get_info/events", "call", {}).then(function (data) {
                console.debug("AJAX receive /ore/get_info/events");
                if (data.error || !_.isUndefined(data.error)) {
                    $scope.error = data.error;
                    console.error($scope.error);
                } else if (_.isEmpty(data)) {
                    $scope.error = "Empty '/ore/get_info/events' data";
                    console.error($scope.error);
                } else {
                    $scope.dct_event_info = data;
                    const arrFromObj = Object.keys(data);
                    $scope.nb_event_info = arrFromObj.length;
                    // $scope.$scope_main.dct_event_info = data;
                    // $scope.$scope_main.nb_event_info = data.length;
                    console.debug($scope.dct_event_info);
                    console.debug($scope.nb_event_info);
                }

                // Process all the angularjs watchers
                $scope.$scope_main.$digest();
                $scope.$digest();
            }).fail(function (error, ev) {
                console.error(error);
                $scope.$scope_main.check_need_login(error);
            })
        }

        $scope.load_all_events();

    }])

    let OREEvent = Widget.extend({
        start: function () {
        },
    });

    return {
        OREEvent: OREEvent,
    };

});
