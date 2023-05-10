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
        $scope.default_section = "monprofil";
        $scope.default_infos_section = "infos";

        $scope.trustSrc = function (src) {
            return $sce.trustAsResourceUrl(src);
        }

        $scope.$on('$locationChangeSuccess', function (object, newLocation, previousLocation) {
            if (window.location.pathname !== "/monprofil") {
                return;
            }

            let sectionParam = {
                "mapresentation": "ma_presentation",
                "mesinfos": "mes_infos",
                "mesannonces": "mes_annonces",
                "mesfavoris": "mes_favoris",
                "mespreferences": "mes_preferences"
            }

            let section = $location.search()["section"];
            $scope.section = sectionParam[section] || $scope.default_section;
        });

        $scope.sizeStateValidated = function (state) {
            let size = 0;
            if (!_.isUndefined(state)) {
                size = state.filter(state => state.validate_bug === "<i class=\"fa fa-check\" style=\"color:#00FF00\"></i>").length;
            }
            return size;
        }

        $scope.sizeGuideEchangeService = function (data, state) {
            let size = 0;
            if (!_.isUndefined(state) && !_.isEmpty(data.state_section)) {
                size = state.filter(state => state.section === Object.keys(data.state_section)[0]).length;
            }
            return size;
        }

        $scope.sizeGuideImplemented = function (state) {
            let size = 0;
            if (!_.isUndefined(state)) {
                size = state.filter(state => !state.not_implemented).length;
            }
            return size;
        }

        $scope.open_all_animation_tab = function (lstState) {
            console.debug("Open all animation in tab")
            console.debug(lstState);
            for (const i in lstState) {
                let state = lstState[i];
                console.debug(state)
                if (!_.isEmpty(state.fast_btn_url)) {
                    window.open(state.fast_btn_guide_url, '_blank');
                }
            }
        }

        $scope.getIconCaract = function (state, dctIcon) {
            let item = [];
            for (const [key, value] of Object.entries(dctIcon)) {
                if ("lst_caract" in state && state.lst_caract.includes(key)) {
                    item.push(value);
                }
            }
            // if (!item.length) {
            //     item.push("fa-dash");
            // }

            return item;
        }

        let url = "/ore/get_help_data/";
        ajax.rpc(url, {}).then(function (data) {
            console.debug("AJAX receive get_help_data");
            if (data.error) {
                $scope.error = data.error;
            } else if (_.isEmpty(data)) {
                $scope.error = "Empty data - " + url;
            } else {
                // Init controller or call change_state_name(name)
                $scope.error = "";
                $scope.data = data.data;
                console.debug(data.data);
            }

            // Process all the angularjs watchers
            $scope.$digest();
        })

    }])

    let OREAide = Widget.extend({
        start: function () {
        },
    });

    return {
        OREProfil: OREProfil,
    };

});
