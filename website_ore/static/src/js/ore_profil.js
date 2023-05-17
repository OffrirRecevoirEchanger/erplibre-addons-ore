odoo.define('website.ore_profil', function (require) {
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

    app.controller('ProfilController', ['$scope', '$location', '$sce', function ($scope, $location, $sce) {
        $scope._ = _;
        $scope.section = "";
        $scope.infos_section = "";
        $scope.error = "";
        $scope.profil_show = "item" // or "table"
        $scope.profil_show_is_concat = "concat" // or "normal"

        // constant
        $scope.default_section = "mon_profil";
        $scope.default_infos_section = "infos";

        $scope.trustSrc = function (src) {
            return $sce.trustAsResourceUrl(src);
        }

        $scope.$on('$locationChangeSuccess', function (object, newLocation, previousLocation) {
            if (window.location.pathname !== "/monprofil") {
                return;
            }
            let section = $location.search()["section"];
            if (!_.isEmpty(section)) {
                $scope.section = section;
            } else {
                $scope.section = $scope.default_section;
            }
        });
    }])

    let OREAide = Widget.extend({
        start: function () {
        },
    });

    return {
        OREProfil: OREProfil,
    };

});
