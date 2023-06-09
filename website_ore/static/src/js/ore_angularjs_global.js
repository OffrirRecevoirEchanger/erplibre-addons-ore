odoo.define('website.ore_angularjs_global', function (require) {
    "use strict";

    require('web.dom_ready');
    let ajax = require('web.ajax');
    let core = require('web.core');
    let session = require('web.session');
    let Widget = require('web.Widget');
    let QWeb = core.qweb;
    let _t = core._t;

    if (["/web/signup", "/web/reset_password"].includes(window.location.pathname)) {
        console.info("Disable AngularJS, this block signup form.")
        document.getElementById("wrapwrap").removeAttribute("ng-app");
        document.getElementById("wrapwrap").removeAttribute("ng-controller");
        return;
    }

    // Get existing module
    let app = angular.module('OREApp');

    app.filter('unsafe', function ($sce) {
        // This allows html generation in view
        return $sce.trustAsHtml;
    });
    app.filter('lengthKeys', function () {
        return function ($sce) {
            return Object.keys($sce).length;
        }
    });
    app.filter('toTitleCase', function () {
        return function ($sce) {
            return $sce.replace(
                /\w\S*/g,
                function (txt) {
                    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
                }
            );
        }
    });
    app.directive("contenteditable", function () {
        return {
            require: "ngModel",
            link: function (scope, element, attrs, ngModel) {

                function read() {
                    ngModel.$setViewValue(element.html());
                }

                ngModel.$render = function () {
                    element.html(ngModel.$viewValue || "");
                };

                element.bind("blur keyup change", function () {
                    scope.$apply(read);
                });
            }
        };
    });

    // sAnimation.registry.affixMenu.include({
    //     /**
    //      * @override
    //      */
    //     start: function () {
    //         var def = this._super.apply(this, arguments);
    //         return def;
    //     },
    //
    //     //--------------------------------------------------------------------------
    //     // Handlers
    //     //--------------------------------------------------------------------------
    //
    //     /**
    //      * @override
    //      */
    //     _onWindowUpdate: function () {
    //         this._super.apply(this, arguments);
    //         if (this.$headerClone) {
    //             // this.$headerClone.each(function () {
    //             // this.$headers.each(function () {
    //             //     let content = $(this);
    //             var content = this.$headerClone;
    //
    //             var content = $("#patate");
    //             var $target = $("[ng-app]");
    //
    //             angular.element($target).injector().invoke(['$compile', function ($compile) {
    //                 var $scope = angular.element($target).scope();
    //
    //                 // $scope.personal.actual_bank_hours += 1;
    //                 // $scope.update_personal_data();
    //
    //                 // let test = $("{{personal.actual_bank_hours}}")
    //                 // $compile(test)($scope);
    //
    //                 $compile(content)($scope);
    //                 // Finally, refresh the watch expressions in the new element
    //                 $scope.$apply();
    //                 console.debug(content);
    //                 // console.debug(test);
    //             }]);
    //
    //         }
    //     },
    // })

    app.controller('MainController', ['$scope', '$http', '$location', function ($scope, $http, $location) {
        $scope._ = _;
        $scope.global = {
            dbname: undefined,
            database: {},
        }
        $scope.personal = {
            // static
            id: undefined,
            is_favorite: false,
            full_name: "-",
            actual_bank_hours: 0,
            actual_month_bank_hours: 0,
            introduction: "",
            description: "",
            interet: [],
            langue: [],
            motivation_membre: "",
            nom: "",
            genre: "",
            date_naissance: "",
            email: "",
            phone: "",
            street: "",
            diff_humain_creation_membre: "",
            antecedent_judiciaire_verifier: false,
            my_network: {
                name: "-",
                id: 0,
            },
            dct_offre_service: {},
            dct_demande_service: {},
            dct_offre_service_favoris: {},
            dct_demande_service_favoris: {},
            dct_membre_favoris: {},
            dct_echange: {},

            // calculate
            actual_bank_sign: true,
            actual_bank_time_diff: "00:00",
            actual_bank_time_human: "+ 0 heure",
            actual_bank_time_human_short: "0h",
            actual_bank_time_human_simplify: "0 heure",
            actual_month_bank_time_human_short: "0h",
            nb_echange_a_venir: 0,
            nb_echange_en_cours: 0,
            nb_echange_passe: 0,
            estPersonnel: true,
            dct_echange_mensuel: {},

            // is_in_offre_service_favoris: function () {
            //     return  $scope.offre_service_info.id in Objects.keys(offre_service_info);
            // },
            // is_in_demande_service_favoris: function () {
            //     return  $scope.demande_service_info.id in Objects.keys(demande_service_info);
            // },
        }
        $scope.membre_info = {}
        $scope.page_presentation_membre_info = {}
        $scope.dct_membre = {}
        $scope.contact_info = {}
        $scope.offre_service_info = {}
        $scope.dct_offre_service_info = {}
        $scope.demande_service_info = {}
        $scope.dct_demande_service_info = {}
        $scope.echange_service_info = {}
        $scope.dct_echange_service_info = {}
        $scope.nb_offre_service = 0;
        $scope.animation_controller_enable = false;
        $scope.url_debug = "";
        $scope.modify_label_when_empty = "Modifiez moi!"
        $scope.language = {
            selected: undefined,
            list: [],
        }

        // TODO créer environnement modification
        $scope.show_croppie = false;
        $scope.ask_modification = false;
        $scope.ask_modification_profile = false;
        $scope.ask_modif_copy = {
            membre_info: {},
            introduction: "",
            full_name: "",
            genre: "",
            date_naissance: "",
            email: "",
            phone: "",
            street: ""
        };
        $scope.list_interets = [];
        $scope.languesParlees = [];
        $scope.afficherAjoutInteret = false;
        $scope.afficherSupprimerInteret = false;
        $scope.afficherAjoutLangue = false;
        $scope.afficherSupprimerLangue = false;
        $scope.nouvelleInteret = '';
        $scope.nouvelleLangue = '';
        $scope.supprimeLangue = '';
        $scope.supprimeInteret = '';
        $scope.interetsCount = 0;
        $scope.languesCount = 0;

        $scope.check_need_login = function (error) {
            if (window.location.pathname !== "" &&
                window.location.pathname !== "/" &&
                window.location.pathname !== "/aide" &&
                window.location.pathname !== "/terms-of-service" &&
                window.location.pathname !== "/privacy-policy" &&
                window.location.pathname !== "/web/login" &&
                window.location.pathname !== "/web/reset_password" &&
                error.data.name === "odoo.http.SessionExpiredException") {
                console.warn("Relocation");
                window.location.href = `/web/login?redirect=${window.location.href}`
            }
        }

        $scope.shouldHideBorder = function (titre) {
            if (titre === "description") {
                return !(
                    !_.isUndefined($scope.membre_info.description) &&
                    !_.isEmpty($scope.membre_info.description)
                );
            } else if (titre === "motivation_membre") {
                return !(
                    !_.isUndefined($scope.membre_info.motivation_membre) &&
                    !_.isEmpty($scope.membre_info.motivation_membre)
                );
            } else if (titre === "interet") {
                return !(
                    !_.isUndefined($scope.membre_info.interet) &&
                    !_.isEmpty($scope.membre_info.interet)
                );
            }
        };

        $scope.ajouterInteret = function () {
            $scope.afficherSupprimerInteret = false;
            $scope.afficherAjoutInteret = true;
        };

        $scope.supprimerInteret = function () {
            $scope.afficherAjoutInteret = false;
            $scope.afficherSupprimerInteret = true;
        };

        $scope.enregistrerInteret = function () {
            if ($scope.nouvelleInteret) {
                if (!$scope.list_interets) {
                    $scope.list_interets = [];
                }
                if (!$scope.membre_info.interet) {
                    $scope.membre_info.interet = [];
                }
                // Check if nouvelleInteret already exists in list_interets or membre_info.interet
                let isNewInteret = $scope.list_interets.indexOf($scope.nouvelleInteret) === -1 &&
                    $scope.membre_info.interet.findIndex(function (interet) {
                        return interet.name === $scope.nouvelleInteret;
                    }) === -1;
                if (isNewInteret) {
                    $scope.list_interets.push($scope.nouvelleInteret);
                    $scope.interetsCount++;
                    $scope.membre_info.interet.push({"name": $scope.nouvelleInteret, "id": 0});
                }
                $scope.afficherAjoutInteret = false;
                $scope.nouvelleInteret = '';
            }
        };


        $scope.annulerModifierInteret = function () {
            $scope.afficherAjoutInteret = false;
            $scope.afficherSupprimerInteret = false;
        }

        $scope.enleverDernieresInterets = function () {
            if ($scope.interetsCount !== 0) {
                $scope.list_interets.splice(-($scope.interetsCount));
            }
            $scope.interetsCount = 0;
        };

        $scope.enleverInteret = function (name) {
            $scope.supprimeInteret = name;
            if ($scope.supprimeInteret) {
                let index = $scope.list_interets.indexOf($scope.supprimeInteret);
                if (index > -1) {
                    $scope.list_interets.splice(index, 1);
                }
                $scope.membre_info.interet = $scope.membre_info.interet.filter(function (interet) {
                    return interet.name !== $scope.supprimeInteret;
                });
            }
        };

        $scope.ajouterLangue = function () {
            $scope.afficherSupprimerLangue = false;
            $scope.afficherAjoutLangue = true;
        };

        $scope.supprimerLangue = function () {
            $scope.afficherAjoutLangue = false;
            $scope.afficherSupprimerLangue = true;
        };

        $scope.enregistrerLangue = function () {
            if ($scope.nouvelleLangue) {
                if (!$scope.languesParlees) {
                    $scope.languesParlees = [];
                }
                if (!$scope.membre_info.langue) {
                    $scope.membre_info.langue = [];
                }
                // Check if nouvelleLangue already exists in languesParlees or membre_info.langue
                let isNewLangue = $scope.languesParlees.indexOf($scope.nouvelleLangue) === -1 &&
                    $scope.membre_info.langue.findIndex(function (langue) {
                        return langue.name === $scope.nouvelleLangue;
                    }) === -1;
                if (isNewLangue) {
                    $scope.languesParlees.push($scope.nouvelleLangue);
                    $scope.languesCount++;
                    $scope.membre_info.langue.push({"name": $scope.nouvelleLangue, "id": 0});
                }
                $scope.afficherAjoutLangue = false;
                $scope.nouvelleLangue = '';
            }
        };


        $scope.annulerModifierLangue = function () {
            $scope.afficherSupprimerLangue = false;
            $scope.afficherAjoutLangue = false;
        }

        $scope.enleverDernieresLangues = function () {
            if ($scope.languesCount !== 0) {
                $scope.languesParlees.splice(-($scope.languesCount));
            }
            $scope.languesCount = 0;
        };

        $scope.enleverLangue = function (name) {
            $scope.supprimeLangue = name;
            if ($scope.supprimeLangue) {
                let index = $scope.languesParlees.indexOf($scope.supprimeLangue);
                if (index > -1) {
                    $scope.languesParlees.splice(index, 1);
                }
                $scope.membre_info.langue = $scope.membre_info.langue.filter(function (langue) {
                    return langue.name !== $scope.supprimeLangue;
                });
            }
        };

        $(document).ready(function () {
            // Define the list of languages
            let languages = [
                "Anglais",
                "Français",
                "Espagnol",
                "Allemand",
                "Turc",
                "Arab",
                "Chinois",
                "Portugais",
                // Add more languages as needed
            ];

            // Initialize the autocomplete for the "nouvelleLangue" input field
            $("#nouvelleLangue").autocomplete({
                source: languages,
            });
            // Initialize the autocomplete for the "supprimeLangue" input field
            $("#supprimeLangue").autocomplete({
                source: languages
            });
        });

        $scope.updateImage = function (input) {
            let reader = new FileReader();
            reader.onload = function () {
                $scope.$apply(function () {
                    $scope.membre_info.ma_photo = reader.result;
                    $scope.show_croppie = true;
                    if ($scope.show_croppie) {
                        let croppie = new Croppie(document.getElementById('profile-picture'), {
                            viewport: {width: 300, height: 300},
                            boundary: {width: 300, height: 300},
                            enableOrientation: true,
                        });
                        croppie.bind({
                            url: $scope.membre_info.ma_photo,
                            orientation: 1
                        });
                        $scope.destroyCroppie = function () {
                            if (croppie) {
                                croppie.destroy();
                            }
                        }
                        $scope.clearData = function () {
                            $scope.membre_info.ma_photo = $scope.ask_modif_copy.membre_info.ma_photo;
                        }
                        $scope.closeModalForm = function () {
                            let modal = document.getElementsByClassName("modal_pub_offre");
                            if (!_.isUndefined(modal) && !_.isEmpty(modal)) {
                                modal[0].setAttribute('aria-hidden', 'true');
                                // c'est nécessaire pour fermer le dialog
                                modal[0].classList.remove('modal_shown');
                                let backdrop = angular.element(document.querySelector(".modal-backdrop"));
                                backdrop.remove();
                                $scope.destroyCroppie();
                            }
                        }
                        $scope.cropProfilePicture = function () {
                            croppie.result('base64', {
                                size: {width: 300, height: 300},
                                type: 'base64',
                                format: 'jpeg',
                                quality: 1
                            }).then(function (result) {
                                $scope.membre_info.ma_photo = result;
                                $scope.show_croppie = false;
                                $scope.closeModalForm();
                            });
                        };
                    }
                });
            };
            reader.readAsDataURL(input.files[0]);
        };

        //Changement des pages de Profil
        $scope.annuler_ask_modification_profile = function () {
            // revert
            $scope.membre_info.ma_photo = $scope.ask_modif_copy.membre_info.ma_photo;
            $scope.membre_info.introduction = $scope.ask_modif_copy.membre_info.introduction;
            $scope.membre_info.description = $scope.ask_modif_copy.membre_info.description;
            $scope.membre_info.interet = $scope.ask_modif_copy.membre_info.interet;
            $scope.membre_info.motivation_membre = $scope.ask_modif_copy.membre_info.motivation_membre;
            $scope.membre_info.langue = $scope.ask_modif_copy.membre_info.langue;
            $scope.ask_modification_profile = false;
            $scope.afficherAjoutLangue = false;
            $scope.afficherSupprimerLangue = false;
            $scope.afficherSupprimerInteret = false;
            $scope.afficherAjoutInteret = false;
            $scope.enleverDernieresLangues();
            $scope.enleverDernieresInterets()
            $scope.show_croppie = false;
        };

        $scope.change_ask_modification_profile = function (enable) {
            console.debug(enable);
            $scope.ask_modification_profile = enable;
            if (!enable) {
                // Recording, check diff and rpc to server
                let form = {};
                if ($scope.ask_modif_copy.membre_info.ma_photo !== $scope.membre_info.ma_photo) {
                    form["ma_photo"] = $scope.membre_info.ma_photo;
                }
                if ($scope.membre_info.introduction === $scope.modify_label_when_empty) {
                    $scope.membre_info.introduction = "";
                }
                if ($scope.ask_modif_copy.membre_info.introduction !== $scope.membre_info.introduction) {
                    form["introduction"] = $scope.membre_info.introduction;
                }
                if ($scope.membre_info.description === $scope.modify_label_when_empty) {
                    $scope.membre_info.description = "";
                }
                if ($scope.ask_modif_copy.membre_info.description !== $scope.membre_info.description) {
                    form["description"] = $scope.membre_info.description;
                }
                if ($scope.membre_info.interet === $scope.modify_label_when_empty) {
                    $scope.membre_info.interet = [];
                }
                if ($scope.ask_modif_copy.membre_info.interet !== $scope.membre_info.interet) {
                    form["interets"] = $scope.list_interets;
                }
                if ($scope.supprimeInteret) {
                    form["supprimeInteret"] = $scope.supprimeInteret;
                }
                if ($scope.membre_info.motivation_membre === $scope.modify_label_when_empty) {
                    $scope.membre_info.motivation_membre = "";
                }
                if ($scope.ask_modif_copy.membre_info.motivation_membre !== $scope.membre_info.motivation_membre) {
                    form["motivation_membre"] = $scope.membre_info.motivation_membre;
                }
                if ($scope.membre_info.langue === $scope.modify_label_when_empty) {
                    $scope.membre_info.langue = [];
                }
                if ($scope.ask_modif_copy.membre_info.langue !== $scope.membre_info.langue) {
                    form["langues"] = $scope.languesParlees;
                }
                if ($scope.supprimeLangue) {
                    form["supprimeLangue"] = $scope.supprimeLangue;
                }
                if (!_.isEmpty(form)) {
                    let url = "/ore/personal_information/submit"
                    ajax.jsonRpc(url, "call", form).then(function (data) {
                            console.debug("AJAX receive submit_form personal_information");
                            console.debug(data);

                            if (data.error) {
                                $scope.error = data.error;
                            } else if (_.isEmpty(data)) {
                                $scope.error = "Empty data - " + url;
                            } else {
                            }
                            // Process all the angularjs watchers
                            $scope.$digest();
                        }
                    ).fail(function (error, ev) {
                        console.error(error);
                        $scope.check_need_login(error);
                    })
                }
                $scope.show_croppie = false;
                $scope.afficherAjoutLangue = false;
                $scope.afficherSupprimerLangue = false;
                $scope.afficherSupprimerInteret = false;
                $scope.afficherAjoutInteret = false;
            } else {
                // Modification, make copy
                // let file = $scope.membre_info.ma_photo;
                if (!_.isUndefined($scope.membre_info.ma_photo)) {
                    $scope.ask_modif_copy.membre_info.ma_photo = JSON.parse(JSON.stringify($scope.membre_info.ma_photo));
                } else {
                    $scope.ask_modif_copy.membre_info.ma_photo = undefined;
                }

                if (!_.isUndefined($scope.membre_info.introduction)) {
                    if (_.isEmpty($scope.membre_info.introduction)) {
                        $scope.membre_info.introduction = $scope.modify_label_when_empty;
                        $scope.ask_modif_copy.membre_info.introduction = "";
                    } else {
                        $scope.ask_modif_copy.membre_info.introduction = JSON.parse(JSON.stringify($scope.membre_info.introduction));
                    }
                } else {
                    $scope.ask_modif_copy.membre_info.introduction = undefined;
                }

                if (!_.isUndefined($scope.membre_info.description)) {
                    if (_.isEmpty($scope.membre_info.description)) {
                        $scope.membre_info.description = $scope.modify_label_when_empty;
                        $scope.ask_modif_copy.membre_info.description = "";
                    } else {
                        $scope.ask_modif_copy.membre_info.description = JSON.parse(JSON.stringify($scope.membre_info.description));
                    }
                } else {
                    $scope.ask_modif_copy.membre_info.description = undefined;
                }

                if (!_.isUndefined($scope.membre_info.interet)) {
                    if (_.isEmpty($scope.membre_info.interet)) {
                        $scope.membre_info.interet = [];
                        $scope.ask_modif_copy.membre_info.interet = [];
                    } else {
                        $scope.ask_modif_copy.membre_info.interet = JSON.parse(JSON.stringify($scope.membre_info.interet));
                    }
                } else {
                    $scope.ask_modif_copy.membre_info.interet = undefined;
                }

                if (!_.isUndefined($scope.membre_info.motivation_membre)) {
                    if (_.isEmpty($scope.membre_info.motivation_membre)) {
                        $scope.membre_info.motivation_membre = $scope.modify_label_when_empty;
                        $scope.ask_modif_copy.membre_info.motivation_membre = "";
                    } else {
                        $scope.ask_modif_copy.membre_info.motivation_membre = JSON.parse(JSON.stringify($scope.membre_info.motivation_membre));
                    }
                } else {
                    $scope.ask_modif_copy.membre_info.motivation_membre = undefined;
                }

                if (!_.isUndefined($scope.membre_info.langue)) {
                    if (_.isEmpty($scope.membre_info.langue)) {
                        $scope.membre_info.langue = [];
                        $scope.ask_modif_copy.membre_info.langue = [];
                    } else {
                        $scope.ask_modif_copy.membre_info.langue = JSON.parse(JSON.stringify($scope.membre_info.langue));
                    }
                } else {
                    $scope.ask_modif_copy.membre_info.langue = undefined;
                }
                $scope.show_croppie = false;
                $scope.afficherAjoutLangue = false;
                $scope.afficherSupprimerLangue = false;
                $scope.afficherSupprimerInteret = false;
                $scope.afficherAjoutInteret = false;
                $scope.languesCount = 0;
                $scope.interetsCount = 0;
            }
        };

        //Page d'Information
        $scope.change_profile_name = function (nom) {
            $scope.ask_modification_profile_nom = nom;

            if (!nom) {
                let form = {};
                if ($scope.ask_modif_copy.membre_info.full_name !== $scope.membre_info.full_name) {
                    form["full_name"] = $scope.membre_info.full_name;
                }
                if (!_.isEmpty(form)) {
                    let url = "/ore/personal_information/submit";
                    ajax.jsonRpc(url, "call", form).then(function (data) {
                        console.debug("AJAX receive submit_form personal_information");
                        console.debug(data);

                        if (data.error) {
                            $scope.error = data.error;
                        } else if (_.isEmpty(data)) {
                            $scope.error = "Empty data - " + url;
                        }
                        // Process all the angularjs watchers
                        $scope.$digest();
                    }).fail(function (error, ev) {
                        console.error(error);
                        $scope.check_need_login(error);
                    })
                }
            } else {
                if (!_.isUndefined($scope.membre_info.full_name)) {
                    if (_.isEmpty($scope.membre_info.full_name)) {
                        $scope.membre_info.full_name = "";
                        $scope.ask_modif_copy.membre_info.full_name = "";
                    } else {
                        $scope.ask_modif_copy.membre_info.full_name = JSON.parse(JSON.stringify($scope.membre_info.full_name));
                    }
                } else {
                    $scope.ask_modif_copy.membre_info.full_name = undefined;
                }
            }
        };

        $scope.annuler_profile_name = function () {
            $scope.membre_info.full_name = $scope.ask_modif_copy.membre_info.full_name;
            $scope.ask_modification_profile_nom = false;
        };

        $scope.change_profile_gender = function (genre) {
            $scope.ask_modification_profile_genre = genre;

            if (!genre) {
                let form = {};
                if ($scope.ask_modif_copy.membre_info.genre !== $scope.membre_info.genre) {
                    let selectedOption = document.getElementById("genre").value;
                    form["genre"] = selectedOption;
                }
                if (!_.isEmpty(form)) {
                    let url = "/ore/personal_information/submit";
                    ajax.jsonRpc(url, "call", form).then(function (data) {
                        console.debug("AJAX receive submit_form personal_information");
                        console.debug(data);

                        if (data.error) {
                            $scope.error = data.error;
                        } else if (_.isEmpty(data)) {
                            $scope.error = "Empty data - " + url;
                        }
                        // Process all the angularjs watchers
                        $scope.$digest();
                    }).fail(function (error, ev) {
                        console.error(error);
                        $scope.check_need_login(error);
                    })
                }
            } else {
                if (!_.isUndefined($scope.membre_info.genre)) {
                    if (_.isEmpty($scope.membre_info.genre)) {
                        $scope.membre_info.genre = "";
                        $scope.ask_modif_copy.membre_info.genre = "";
                    } else {
                        $scope.ask_modif_copy.membre_info.genre = JSON.parse(JSON.stringify($scope.membre_info.genre));
                    }
                } else {
                    $scope.ask_modif_copy.membre_info.genre = undefined;
                }
            }
        };

        $scope.annuler_profile_gender = function () {
            $scope.membre_info.genre = $scope.ask_modif_copy.membre_info.genre;
            $scope.ask_modification_profile_genre = false;
        };

        $scope.change_profile_date_naissance = function (date) {
            $scope.ask_modification_profile_date = date;

            if (!date) {
                let form = {};
                if ($scope.membre_info.date_naissance === "") {
                    $scope.membre_info.date_naissance = "";
                }
                if ($scope.ask_modif_copy.membre_info.date_naissance !== $scope.membre_info.date_naissance) {
                    form["date_naissance"] = $scope.membre_info.date_naissance;
                }
                if (!_.isEmpty(form)) {
                    let url = "/ore/personal_information/submit";
                    ajax.jsonRpc(url, "call", form).then(function (data) {
                        console.debug("AJAX receive submit_form personal_information");
                        console.debug(data);

                        if (data.error) {
                            $scope.error = data.error;
                        } else if (_.isEmpty(data)) {
                            $scope.error = "Empty data - " + url;
                        }
                        // Process all the angularjs watchers
                        $scope.$digest();
                    }).fail(function (error, ev) {
                        console.error(error);
                        $scope.check_need_login(error);
                    })
                }
            } else {
                if (!_.isUndefined($scope.membre_info.date_naissance)) {
                    if (_.isEmpty($scope.membre_info.date_naissance)) {
                        $scope.membre_info.date_naissance = "";
                        $scope.ask_modif_copy.membre_info.date_naissance = "";
                    } else {
                        $scope.ask_modif_copy.membre_info.date_naissance = JSON.parse(JSON.stringify($scope.membre_info.date_naissance));
                    }
                } else {
                    $scope.ask_modif_copy.membre_info.date_naissance = undefined;
                }
            }
        };

        $scope.annuler_profile_date = function () {
            $scope.membre_info.date_naissance = $scope.ask_modif_copy.membre_info.date_naissance;
            $scope.ask_modification_profile_date = false;
        };

        $scope.change_profile_email = function (email) {
            $scope.ask_modification_profile_email = email;

            if (!email) {
                let form = {};
                if ($scope.ask_modif_copy.membre_info.email !== $scope.membre_info.email) {
                    if (!$scope.membre_info.email) {
                        return;
                    } else {
                        form["email"] = $scope.membre_info.email;
                    }
                }
                if (!_.isEmpty(form)) {
                    let url = "/ore/personal_information/submit";
                    ajax.jsonRpc(url, "call", form).then(function (data) {
                        console.debug("AJAX receive submit_form personal_information");
                        console.debug(data);

                        if (data.error) {
                            $scope.error = data.error;
                        } else if (_.isEmpty(data)) {
                            $scope.error = "Empty data - " + url;
                        }
                        // Process all the angularjs watchers
                        $scope.$digest();
                    }).fail(function (error, ev) {
                        console.error(error);
                        $scope.check_need_login(error);
                    })
                }
            } else {
                if (!_.isUndefined($scope.membre_info.email)) {
                    if (_.isEmpty($scope.membre_info.email)) {
                        $scope.membre_info.email = "";
                        $scope.ask_modif_copy.membre_info.email = "";
                    } else {
                        $scope.ask_modif_copy.membre_info.email = JSON.parse(JSON.stringify($scope.membre_info.email));
                    }
                } else {
                    $scope.ask_modif_copy.membre_info.email = undefined;
                }
            }
        };

        $scope.annuler_profile_email = function () {
            console.log("TEST");
            $scope.membre_info.email = $scope.ask_modif_copy.membre_info.email;
            $scope.ask_modification_profile_email = false;
        };

        $scope.change_profile_telephone = function (telephone) {
            $scope.ask_modification_profile_telephone = telephone;

            if (!telephone) {
                let form = {};
                if ($scope.ask_modif_copy.membre_info.phone !== $scope.membre_info.phone) {
                    form["phone"] = $scope.membre_info.phone;
                }
                if (!_.isEmpty(form)) {
                    let url = "/ore/personal_information/submit";
                    ajax.jsonRpc(url, "call", form).then(function (data) {
                        console.debug("AJAX receive submit_form personal_information");
                        console.debug(data);

                        if (data.error) {
                            $scope.error = data.error;
                        } else if (_.isEmpty(data)) {
                            $scope.error = "Empty data - " + url;
                        }
                        // Process all the angularjs watchers
                        $scope.$digest();
                    }).fail(function (error, ev) {
                        console.error(error);
                        $scope.check_need_login(error);
                    })
                }
            } else {
                if (!_.isUndefined($scope.membre_info.phone)) {
                    if (_.isEmpty($scope.membre_info.phone)) {
                        $scope.membre_info.phone = "";
                        $scope.ask_modif_copy.membre_info.phone = "";
                    } else {
                        $scope.ask_modif_copy.membre_info.phone = JSON.parse(JSON.stringify($scope.membre_info.phone));
                    }
                } else {
                    $scope.ask_modif_copy.membre_info.phone = undefined;
                }
            }
        };

        $scope.annuler_profile_telephone = function () {

            $scope.membre_info.phone = $scope.ask_modif_copy.membre_info.phone;
            $scope.ask_modification_profile_telephone = false;
        };

        $scope.change_profile_street = function (street) {
            $scope.ask_modification_profile_street = street;

            if (!street) {
                let form = {};
                if ($scope.ask_modif_copy.membre_info.street !== $scope.membre_info.street) {
                    form["street"] = $scope.membre_info.street;
                }
                if (!_.isEmpty(form)) {
                    let url = "/ore/personal_information/submit";
                    ajax.jsonRpc(url, "call", form).then(function (data) {
                        console.debug("AJAX receive submit_form personal_information");
                        console.debug(data);

                        if (data.error) {
                            $scope.error = data.error;
                        } else if (_.isEmpty(data)) {
                            $scope.error = "Empty data - " + url;
                        }
                        // Process all the angularjs watchers
                        $scope.$digest();
                    }).fail(function (error, ev) {
                        console.error(error);
                        $scope.check_need_login(error);
                    })
                }
            } else {
                if (!_.isUndefined($scope.membre_info.street)) {
                    if (_.isEmpty($scope.membre_info.street)) {
                        $scope.membre_info.street = "";
                        $scope.ask_modif_copy.membre_info.street = "";
                    } else {
                        $scope.ask_modif_copy.membre_info.street = JSON.parse(JSON.stringify($scope.membre_info.street));
                    }
                } else {
                    $scope.ask_modif_copy.membre_info.street = undefined;
                }
            }
        };

        $scope.annuler_profile_street = function () {
            $scope.membre_info.street = $scope.ask_modif_copy.membre_info.street;
            $scope.ask_modification_profile_street = false;
        };
        //END

        $scope.isEmailEmpty = function () {
            return _.isEmpty($scope.membre_info.email);
        };
        // End modification environnement

        // History
        $scope.$on('$locationChangeSuccess', function (object, newLocation, previousLocation) {
            if (window.location.search === "?debug=assets") {
                $scope.url_debug = "?debug=assets";
            }
            if (window.location.pathname !== "/monactivite/echange") {
                return;
            }
            if (newLocation !== previousLocation) {
                let new_echange_id = $location.search()["echange"];
                if (!_.isUndefined(new_echange_id)) {
                    $scope.update_echange_service();
                }
            }
        });

        $scope.lst_notification = [];

        $scope.notif_filter_unread = function (notif) {
            return !_.isUndefined(notif.is_read) && !notif.is_read;
        }

        $scope.toggle_animation_record_show = function () {
            $scope.animation_controller_enable = !$scope.animation_controller_enable;
            let $scope_animation = angular.element(document.querySelector('[ng-controller="AnimationController"]')).scope();
            $scope_animation.animationRecord.enable = $scope.animation_controller_enable;
        }

        $scope.add_to_my_favorite_field_id = function (model, record_id) {
            ajax.jsonRpc("/ore/submit/my_favorite", "call", {
                "model": model,
                "id_record": record_id
            }).then(function (data) {
                console.debug("AJAX receive add_to_my_favorite");
                if (data.error || !_.isUndefined(data.error)) {
                    $scope.error = data.error;
                    console.error($scope.error);
                } else if (_.isEmpty(data)) {
                    $scope.error = "Empty 'add_to_my_favorite' data";
                    console.error($scope.error);
                } else {
                    // $scope.nb_offre_service = data.nb_offre_service;
                    // record_obj.is_favorite = data.is_favorite;
                    // if (model === "ore.membre" && data.is_favorite) {
                    //     // TODO validate not already in list
                    //     $scope.personal.lst_membre_favoris.push(record_obj);
                    // }
                }

                // Process all the angularjs watchers
                $scope.$digest();
            }).fail(function (error, ev) {
                console.error(error);
                $scope.check_need_login(error);
            })
        }

        $scope.supprimer_offre_service = function (offre_id) {
            ajax.jsonRpc(`/ore/submit/offre/supprimer/${offre_id}`, "call", {}).then(function (data) {
                console.debug("AJAX receive supprimer_offre_service");
                if (data.error || !_.isUndefined(data.error)) {
                    $scope.error = data.error;
                    console.error($scope.error);
                    // } else if (_.isEmpty(data)) {
                    //     $scope.error = "Empty 'add_to_my_favorite' data";
                    //     console.error($scope.error);
                } else {
                    // Change location because it's deleted
                    location.replace("/monprofil/mesannonces");
                }

                // Process all the angularjs watchers
                // $scope.$digest();
            }).fail(function (error, ev) {
                console.error(error);
                $scope.check_need_login(error);
            })
        }

        $scope.supprimer_demande_service = function (demande_id) {
            ajax.jsonRpc(`/ore/submit/demande/supprimer/${demande_id}`, "call", {}).then(function (data) {
                console.debug("AJAX receive supprimer_demande_service");
                if (data.error || !_.isUndefined(data.error)) {
                    $scope.error = data.error;
                    console.error($scope.error);
                    // } else if (_.isEmpty(data)) {
                    //     $scope.error = "Empty 'add_to_my_favorite' data";
                    //     console.error($scope.error);
                } else {
                    // Change location because it's deleted
                    location.replace("/monprofil/mesannonces");
                }

                // Process all the angularjs watchers
                // $scope.$digest();
            }).fail(function (error, ev) {
                console.error(error);
                $scope.check_need_login(error);
            })
        }

        $scope.change_publication_offre_service = function (offre_id, website_published) {
            ajax.jsonRpc(`/ore/submit/offre/publish/${offre_id}`, "call", {"website_published": website_published}).then(function (data) {
                console.debug("AJAX receive change_publication_offre_service");
                if (data.error || !_.isUndefined(data.error)) {
                    $scope.error = data.error;
                    console.error($scope.error);
                    // } else if (_.isEmpty(data)) {
                    //     $scope.error = "Empty 'add_to_my_favorite' data";
                    //     console.error($scope.error);
                }

                // Process all the angularjs watchers
                // $scope.$digest();
            }).fail(function (error, ev) {
                console.error(error);
                $scope.check_need_login(error);
            })
        }

        $scope.change_publication_demande_service = function (demande_id, website_published) {
            ajax.jsonRpc(`/ore/submit/demande/publish/${demande_id}`, "call", {"website_published": website_published}).then(function (data) {
                console.debug("AJAX receive change_publication_demande_service");
                if (data.error || !_.isUndefined(data.error)) {
                    $scope.error = data.error;
                    console.error($scope.error);
                    // } else if (_.isEmpty(data)) {
                    //     $scope.error = "Empty 'add_to_my_favorite' data";
                    //     console.error($scope.error);
                }

                // Process all the angularjs watchers
                // $scope.$digest();
            }).fail(function (error, ev) {
                console.error(error);
                $scope.check_need_login(error);
            })
        }

        // Date
        $scope.load_date = function () {
            let time = require("web.time");
            // TODO not optimal how this is called, need only to be call 1 time when page is loaded (with date)
            console.debug("Call load_date");
            _.each($(".input-group.date"), function (date_field) {
                let minDate =
                    $(date_field).data("mindate") || moment({y: 1900});
                if ($(date_field).attr("date-min-today")) {
                    minDate = moment();
                }
                let maxDate =
                    $(date_field).data("maxdate") || moment().add(200, "y");
                if ($(date_field).attr("date-max-year")) {
                    maxDate = moment().add(1, "y").add(1, "d");
                }
                let inline =
                    $(date_field).attr("inline-date") && true || false;
                let sideBySide =
                    $(date_field).attr("side-by-side") && true || false;
                let calendarWeeks =
                    $(date_field).attr("calendar-weeks") && true || false;
                let dateFormatTool =
                    $(date_field).attr("date-format-tool") || false;

                let options = {
                    minDate: minDate,
                    maxDate: maxDate,
                    calendarWeeks: calendarWeeks,
                    icons: {
                        time: "fa fa-clock-o",
                        date: "fa fa-calendar",
                        next: "fa fa-chevron-right",
                        previous: "fa fa-chevron-left",
                        up: "fa fa-chevron-up",
                        down: "fa fa-chevron-down",
                    },
                    locale: moment.locale(),
                    allowInputToggle: true,
                    inline: inline,
                    sideBySide: sideBySide,
                    keyBinds: null,
                };
                if ($(date_field).find(".o_website_form_date").length > 0 || dateFormatTool === "date") {
                    options.format = time.getLangDateFormat();
                    if (["date_service_datepicker"].includes(date_field.id)) {
                        options.defaultDate = moment();
                    }
                } else if (
                    $(date_field).find(".o_website_form_clock").length > 0 || dateFormatTool === "clock"
                ) {
                    // options.format = time.getLangTimeFormat();
                    options.format = "HH:mm";
                    if (["time_service_datepicker", "time_service"].includes(date_field.id)) {
                        options.defaultDate = moment("08:00", "HH:mm");
                    } else {
                        options.defaultDate = moment("00:00", "HH:mm");
                    }
                } else {
                    options.format = time.getLangDatetimeFormat();
                }
                $("#" + date_field.id).datetimepicker(options);
            });
        }

        $scope.demander_un_service_sur_une_offre = function () {
            let input = $('#date_echange_id');
            let date_value = input.data().date;
            if (date_value.includes("/")) {
                // Bug, wrong format (why, load_date is called with specific format...), force it
                console.warn("Bug wrong format date, got '" + date_value + "' and expect format YYYY-MM-DD, force conversion.")
                date_value = moment(date_value).format("YYYY-MM-DD");
            }
            let membre_id = $scope.offre_service_info.membre_id;
            let offre_id = $scope.offre_service_info.id;
            let url = `/participer${$scope.url_debug}#!?state=init.saa.recevoir.choix.existant.time&membre=${membre_id}&offre_service=${offre_id}&date=${date_value}`;
            console.debug(url);
            // location.replace(url);
            window.location.href = url;
        }

        $scope.offrir_un_service_sur_une_demande = function () {
            let input = $('#date_echange_id');
            let date_value = input.data().date;
            if (date_value.includes("/")) {
                // Bug, wrong format (why, load_date is called with specific format...), force it
                console.warn("Bug wrong format date, got '" + date_value + "' and expect format YYYY-MM-DD, force conversion.")
                date_value = moment(date_value).format("YYYY-MM-DD");
            }
            let membre_id = $scope.demande_service_info.membre_id;
            let demande_id = $scope.demande_service_info.id;
            let url = `/participer${$scope.url_debug}#!?state=init.saa.offrir.demande.existante.date.time.form&membre=${membre_id}&demande_service=${demande_id}&date=${date_value}`;
            console.debug(url);
            // location.replace(url);
            window.location.href = url;
        }

        // Map
        $scope.show_map_member = false;

        // Share
        $scope.show_qrcode_modal = false;

        $scope.show_and_generate_qrcode = function () {
            $scope.show_qrcode_modal = true;
            let urlToCopy = $location.$$absUrl;
            let qrcode_dom = document.getElementById("qrcode");
            // Force clean old QR Code
            qrcode_dom.innerHTML = "";
            new QRCode(qrcode_dom, urlToCopy);
        }

        $scope.show_camera_qrcode_modal = false;
        $scope.list_camera_qrcode = [];
        $scope.show_camera_error = "";
        $scope.selectedCamera = undefined;
        $scope.show_camera_find_url = false;
        $scope.show_camera_link_find = undefined;
        $scope.html5QrCode = undefined;

        $scope.show_camera_select = function (option) {
            $scope.selectedCamera = option;
            $scope.show_camera_open();
        }

        $scope.show_camera_close = function () {
            if (!_.isUndefined($scope.html5QrCode)) {
                // TODO wrong technique to stop camera, use async method
                $scope.html5QrCode.stop().then((ignore) => {
                    // QR Code scanning is stopped.
                    $scope.html5QrCode = undefined;
                }).catch((err) => {
                    // Stop failed, handle it.
                });
            }
            $scope.show_camera_qrcode_modal = false
        }

        $scope.show_camera_qrcode = function () {
            $scope.show_camera_qrcode_modal = true;
            $scope.list_camera_qrcode = [];
            $scope.show_camera_error = "";
            $scope.selectedCamera = undefined;
            $scope.show_camera_link_find = undefined;
            Html5Qrcode.getCameras().then(devices => {
                /**
                 * devices would be an array of objects of type:
                 * { id: "id", label: "label" }
                 */
                $scope.list_camera_qrcode = devices;
                $scope.selectedCamera = devices[devices.length - 1];
                $scope.show_camera_open();
                $scope.$apply();
            }).catch(err => {
                $scope.show_camera_error = err;
                console.error(err);
                $scope.$apply();
            });
        }

        $scope.show_camera_open = function () {
            const html5QrCode = new Html5Qrcode(/* element id */ "reader");
            $scope.html5QrCode = html5QrCode;
            html5QrCode.start(
                $scope.selectedCamera.id,
                {
                    fps: 10,    // Optional, frame per seconds for qr code scanning
                    qrbox: {width: 250, height: 250}  // Optional, if you want bounded box UI
                },
                (decodedText, decodedResult) => {
                    // do something when code is read
                    $scope.show_camera_find_text(decodedText);
                },
                (errorMessage) => {
                    // parse error, ignore it.
                })
                .catch((err) => {
                    // Start failed, handle it.
                    console.error(err);
                    $scope.show_camera_error = err;
                    $scope.$apply();
                });
        }

        $scope.show_camera_find_text = function (decodedText) {
            $scope.show_camera_link_find = decodedText;
            // ignore 'www.'
            let decodedTextCut = decodedText.replace("www.", "");
            let locationText = window.location.origin.replace("www.", "");
            if (decodedTextCut.startsWith(locationText)) {
                // Find good link
                // TODO wrong technique to stop camera, use async method
                $scope.html5QrCode.stop().then((ignore) => {
                    // QR Code scanning is stopped.
                    $scope.html5QrCode = undefined;
                }).catch((err) => {
                    // Stop failed, handle it.
                });
                $scope.show_camera_error = "";
                $scope.show_camera_find_url = true;
                setTimeout(function () {
                    // location.replace(decodedText);
                    window.location.href = decodedText;
                }, 2000);
            } else {
                $scope.show_camera_error = "Le lien est erroné, provient-il de ce site?";
            }
            $scope.$apply();
        }

        $scope.error_copy = "";
        $scope.is_copied_url = false;
        $scope.copy_clipboard_url = function () {
            $scope.error_copy = "";
            $scope.is_copied_url = false;
            let urlToCopy = $location.$$absUrl;
            navigator.clipboard.writeText(urlToCopy).then(() => {
                $scope.is_copied_url = true;
            }, () => {
                $scope.error_copy = "Cannot copy URL";
            });
        }

        $scope.error_share = "";

        $scope.is_share_enable = function () {
            if (!navigator.canShare) {
                return false;
            }
            let urlToShare = $location.$$absUrl;
            let value = {title: "Page ORE", url: urlToShare}
            return navigator.canShare(value)
        }

        $scope.share_link = function () {
            if ($scope.is_share_enable()) {
                $scope.error_share = "";
                let urlToShare = $location.$$absUrl;
                let value = {title: "Page ORE", url: urlToShare}
                try {
                    navigator.share(value);
                } catch (err) {
                    $scope.error_share = err;
                }
            }
        }

        // End Share

        $scope.add_to_my_favorite = function (model, record_obj) {
            let id_record = record_obj.id;
            ajax.jsonRpc("/ore/submit/my_favorite", "call", {
                "model": model,
                "id_record": id_record
            }).then(function (data) {
                console.debug("AJAX receive add_to_my_favorite");
                if (data.error || !_.isUndefined(data.error)) {
                    $scope.error = data.error;
                    console.error($scope.error);
                } else if (_.isEmpty(data)) {
                    $scope.error = "Empty 'add_to_my_favorite' data";
                    console.error($scope.error);
                } else {
                    // $scope.nb_offre_service = data.nb_offre_service;
                    record_obj.is_favorite = data.is_favorite;
                    // if (model === "ore.membre" && data.is_favorite) {
                    //     // TODO validate not already in list
                    //     $scope.personal.lst_membre_favoris.push(record_obj);
                    // }
                }

                // Process all the angularjs watchers
                $scope.$digest();
            }).fail(function (error, ev) {
                console.error(error);
                $scope.check_need_login(error);
            })
        }

        $scope.update_db_my_personal_info = function () {
            ajax.jsonRpc("/ore/get_personal_information", "call", {}).then(function (data) {
                console.debug("AJAX receive get_personal_information");
                if (data.error || !_.isUndefined(data.error)) {
                    $scope.error = data.error;
                    console.error($scope.error);
                } else if (_.isEmpty(data)) {
                    $scope.error = "Empty 'get_personal_information' data";
                    console.error($scope.error);
                } else {
                    $scope.error = "";
                    $scope.global = data.global;
                    $scope.personal = data.personal;
                    $scope.lst_notification = data.lst_notification;

                    $scope.update_personal_data();
                    console.debug($scope.personal);

                    if (!_.isUndefined($scope.personal.my_network)) {
                        $scope.update_db_list_membre($scope.personal.my_network.id);
                    } else {
                        console.error("Cannot associate personal variable with his network data. " +
                            "Talk to an administrator, your are lost!");
                    }

                    // Special case, when need to get information of another member
                    let membre_id = $location.search()["membre_id"];
                    let membre_id_int = parseInt(membre_id);
                    $scope.membre_info = $scope.personal;
                    if (window.location.pathname === "/monprofil/mapresentation" && !_.isUndefined(membre_id) && membre_id_int !== $scope.personal.id) {
                        // Force switch to another user
                        $scope.update_membre_info(membre_id_int, "page_presentation_membre_info");
                    } else {
                        console.debug("Setup membre personal.");
                        $scope.personal.estPersonnel = true;
                        $scope.page_presentation_membre_info = $scope.membre_info;
                    }
                }

                // Process all the angularjs watchers
                $scope.$digest();
            }).fail(function (error, ev) {
                console.error(error);
                $scope.check_need_login(error);
            })
        }

        $scope.update_db_my_personal_info();

        $scope.update_membre_info = function (membre_id, scope_var_name_to_update) {
            ajax.jsonRpc("/ore/get_membre_information/" + membre_id, "call", {}).then(function (data) {
                console.debug("AJAX receive get_membre_information");
                if (data.error || !_.isUndefined(data.error)) {
                    $scope.error = data.error;
                    console.error($scope.error);
                } else if (_.isEmpty(data)) {
                    $scope.error = "Empty 'get_membre_information' data";
                    console.error($scope.error);
                } else {
                    $scope.error = "";
                    data.membre_info.estPersonnel = false;
                    data.membre_info.show_date_creation = moment(data.date_creation).format("MMMM YYYY");
                    data.membre_info.show_bank_max_service_offert = $scope.convertNumToTime(data.membre_info.bank_max_service_offert, 4);
                    $scope[scope_var_name_to_update] = data.membre_info;
                    console.debug(data.membre_info);
                }
                // Process all the angularjs watchers
                $scope.$digest();
            }).fail(function (error, ev) {
                console.error(error);
                $scope.check_need_login(error);
            })
        }

        $scope.get_href_participer_service_effectue = function (echange_service_info) {
            let status
            // if (!_.isUndefined(echange_service_info.demande_service) && !echange_service_info.estAcheteur) {
            //     status = `/participer#!?state=init.va.oui.form&echange_service=${echange_service_info.id}`;
            // } else if (echange_service_info.estAcheteur) {
            //     // TODO why need member?
            //     status = `/participer#!?state=init.va.non.recu.choix.form&membre=${echange_service_info.membre_id}&echange_service=${echange_service_info.id}`;
            // } else {
            //     status = `/participer#!?state=init.va.non.offert.existant.form&membre=${echange_service_info.membre_id}&echange_service=${echange_service_info.id}`;
            // }
            status = `/participer${$scope.url_debug}#!?state=init.va.oui.form&echange_service=${echange_service_info.id}`;
            return status;
        }

        $scope.update_db_nb_offre_service = function () {
            ajax.jsonRpc("/ore/get_info/nb_offre_service", "call", {}).then(function (data) {
                console.debug("AJAX receive get_nb_offre_service");
                if (data.error || !_.isUndefined(data.error)) {
                    $scope.error = data.error;
                    console.error($scope.error);
                } else if (_.isEmpty(data)) {
                    $scope.error = "Empty 'get_nb_offre_service' data";
                    console.error($scope.error);
                } else {
                    $scope.nb_offre_service = data.nb_offre_service;
                }

                // Process all the angularjs watchers
                $scope.$digest();
            }).fail(function (error, ev) {
                console.error(error);
                $scope.check_need_login(error);
            })
        }

        $scope.load_page_offre_demande_echange_service = function () {
            let key = "/ore/ore_offre_service/";
            if (window.location.pathname.indexOf(key) === 0) {
                // params can be 6?debug=1 or 6#!?str=3, need to extract first int
                let params = window.location.pathname.substring(key.length);
                params = parseInt(params, 10);
                if (!Number.isNaN(params)) {
                    ajax.jsonRpc("/ore/get_info/get_offre_service/" + params, "call", {}).then(function (data) {
                        console.debug("AJAX receive /ore/get_info/get_offre_service");
                        if (data.error || !_.isUndefined(data.error)) {
                            $scope.error = data.error;
                            console.error($scope.error);
                        } else if (_.isEmpty(data)) {
                            $scope.error = "Empty '/ore/get_info/get_offre_service' data";
                            console.error($scope.error);
                        } else {
                            $scope.offre_service_info = data;
                            $scope.update_membre_info($scope.offre_service_info.membre_id, "contact_info");
                        }

                        // Process all the angularjs watchers
                        $scope.$digest();
                    }).fail(function (error, ev) {
                        console.error(error);
                        $scope.check_need_login(error);
                    })
                }
            }
            // Remove optimisation, need it for "my favorite"
            // key = "/offresservice";
            // if (window.location.pathname.indexOf(key) === 0) {
            ajax.jsonRpc("/ore/get_info/all_offre_service", "call", {}).then(function (data) {
                console.debug("AJAX receive /ore/get_info/all_offre_service");
                if (data.error || !_.isUndefined(data.error)) {
                    $scope.error = data.error;
                    console.error($scope.error);
                } else if (_.isEmpty(data)) {
                    $scope.error = "Empty '/ore/get_info/all_offre_service' data";
                    console.error($scope.error);
                } else {
                    $scope.dct_offre_service_info = data;
                }

                // Process all the angularjs watchers
                $scope.$digest();
            }).fail(function (error, ev) {
                console.error(error);
                $scope.check_need_login(error);
            })
            // }
            // key = "/demandesservice";
            // if (window.location.pathname.indexOf(key) === 0) {
            ajax.jsonRpc("/ore/get_info/all_demande_service", "call", {}).then(function (data) {
                console.debug("AJAX receive /ore/get_info/all_demande_service");
                if (data.error || !_.isUndefined(data.error)) {
                    $scope.error = data.error;
                    console.error($scope.error);
                } else if (_.isEmpty(data)) {
                    $scope.error = "Empty '/ore/get_info/all_demande_service' data";
                    console.error($scope.error);
                } else {
                    $scope.dct_demande_service_info = data;
                }

                // Process all the angularjs watchers
                $scope.$digest();
            }).fail(function (error, ev) {
                console.error(error);
                $scope.check_need_login(error);
            })
            // }
            key = "/ore/ore_demande_service/";
            if (window.location.pathname.indexOf(key) === 0) {
                // params can be 6?debug=1 or 6#!?str=3, need to extract first int
                let params = window.location.pathname.substring(key.length);
                params = parseInt(params, 10);
                if (!Number.isNaN(params)) {
                    ajax.jsonRpc("/ore/get_info/get_demande_service/" + params, "call", {}).then(function (data) {
                        console.debug("AJAX receive /ore/get_info/get_demande_service");
                        if (data.error || !_.isUndefined(data.error)) {
                            $scope.error = data.error;
                            console.error($scope.error);
                        } else if (_.isEmpty(data)) {
                            $scope.error = "Empty '/ore/get_info/get_demande_service' data";
                            console.error($scope.error);
                        } else {
                            $scope.demande_service_info = data;
                            $scope.update_membre_info($scope.demande_service_info.membre_id, "contact_info");
                        }

                        // Process all the angularjs watchers
                        $scope.$digest();
                    }).fail(function (error, ev) {
                        console.error(error);
                        $scope.check_need_login(error);
                    })
                }
            }
            $scope.update_echange_service();
        }

        $scope.update_echange_service = function () {
            let echange_id = $location.search()["echange"];
            if (!_.isEmpty(echange_id)) {
                echange_id = parseInt(echange_id, 10);
                if (!Number.isNaN(echange_id)) {
                    ajax.jsonRpc("/ore/get_info/get_echange_service/" + echange_id, "call", {}).then(function (data) {
                        console.debug("AJAX receive /ore/get_info/get_echange_service");
                        if (data.error || !_.isUndefined(data.error)) {
                            $scope.error = data.error;
                            console.error($scope.error);
                        } else if (_.isEmpty(data)) {
                            $scope.error = "Empty '/ore/get_info/get_echange_service' data";
                            console.error($scope.error);
                        } else {
                            $scope.echange_service_info = data;

                            let sign = data.estAcheteur ? -1 : 1;
                            $scope.echange_service_info.sign = sign;
                            $scope.echange_service_info.show_duree_estime = $scope.convertNumToTime(data.duree_estime * sign, 7);
                            $scope.echange_service_info.show_duree = $scope.convertNumToTime(data.duree * sign, 7);
                            $scope.echange_service_info.show_duree_trajet_estime = $scope.convertNumToTime(data.duree_trajet_estime * sign, 7);
                            $scope.echange_service_info.show_duree_trajet = $scope.convertNumToTime(data.duree_trajet * sign, 7);
                            $scope.echange_service_info.show_duree_estime_pos = $scope.convertNumToTime(data.duree_estime, 8);
                            $scope.echange_service_info.show_duree_pos = $scope.convertNumToTime(data.duree, 8);
                            $scope.echange_service_info.show_duree_trajet_estime_pos = $scope.convertNumToTime(data.duree_trajet_estime, 8);
                            $scope.echange_service_info.show_duree_trajet_pos = $scope.convertNumToTime(data.duree_trajet, 8);

                            $scope.echange_service_info.show_total_dure_estime = $scope.convertNumToTime(data.duree_estime + data.duree_trajet_estime, 7);
                            $scope.echange_service_info.show_total_dure = $scope.convertNumToTime(data.duree + data.duree_trajet, 7);
                            $scope.echange_service_info.show_total_dure_estime_pos = $scope.convertNumToTime(data.duree_estime + data.duree_trajet_estime, 8);
                            $scope.echange_service_info.show_total_dure_pos = $scope.convertNumToTime(data.duree + data.duree_trajet, 8);

                            $scope.echange_service_info.show_date = moment(data.date).format("dddd D MMMM");
                            $scope.echange_service_info.show_start_time = moment(data.date).format("H") + "h" + moment(data.date).format("mm");
                            $scope.echange_service_info.show_end_time = moment(data.end_date).format("H") + "h" + moment(data.end_date).format("mm");

                            $scope.update_membre_info($scope.echange_service_info.membre_id, "contact_info");

                            console.debug($scope.echange_service_info);
                        }

                        // Process all the angularjs watchers
                        $scope.$digest();
                    }).fail(function (error, ev) {
                        console.error(error);
                        $scope.check_need_login(error);
                    })
                }
            }
        }

        $scope.load_page_offre_demande_echange_service();

        $scope.update_db_list_membre = function (reseau_ore_id) {
            ajax.jsonRpc("/ore/get_info/list_membre", "call", {"reseau_ore_id": reseau_ore_id}).then(function (data) {
                console.debug("AJAX receive /ore/get_info/list_membre");
                if (data.error || !_.isUndefined(data.error)) {
                    $scope.error = data.error;
                    console.error($scope.error);
                } else if (_.isEmpty(data)) {
                    $scope.error = "Empty '/ore/get_info/list_membre' data";
                    console.error($scope.error);
                } else {
                    console.debug(data.dct_membre);
                    $scope.dct_membre = data.dct_membre;
                }

                // Process all the angularjs watchers
                $scope.$digest();
            }).fail(function (error, ev) {
                console.error(error);
                $scope.check_need_login(error);
            })
        }

        $scope.update_db_nb_offre_service();

        $scope.getDatabaseInfo = function (model, field_id) {
            // TODO compete this, suppose to update database value and use cache
            if (model === "ore.offre.service") {
                return $scope.dct_offre_service_info[field_id];
            } else if (model === "ore.demande.service") {
                return $scope.dct_demande_service_info[field_id];
            }
        }

        // $scope.forceRefreshAngularJS = function () {
        //     // console.debug("Force refresh AngularJS");
        //     // $scope.$digest();
        //     compileAngularElement(".o_affix_enabled");
        // }

        $scope.convertNumToTime = function (number, format = 0) {
            // format 0 : 1.0 -> 1:00, 1.75 -> 1:45, -.75 -> -0:45
            // format 1 : 1.0 -> +1:00, 1.75 -> +1:45, -.75 -> -0:45
            // format 2 : 1.0 -> + 1:00, 1.75 -> + 1:45, -.75 -> - 0:45
            // format 3 : 1.0 -> + 1h, 1.75 -> + 1h45, -.75 -> - 0h45
            // format 4 : 1.0 -> 1h, 1.75 -> 1h45, -.75 -> -0h45
            // format 5 : 2.0 -> + 2 heures, 1.75 -> + 1 heure 45, -.75 -> - 0 heure 45
            // format 6 : 2.0 -> 2 heures, 1.75 -> 1 heure 45, -.75 -> - 0 heure 45
            // format 7 : 1.0 -> + 1h00, 1.75 -> + 1h45, -.75 -> - 0h45
            // format 8 : 1.0 -> 1h00, 1.75 -> + 1h45, -.75 -> - 0h45
            // format 9 : 1.0 -> 01:00, 1.75 -> 01:45, -.75 -> -00:45

            if (format > 9 || format < 0) {
                format = 0;
            }

            // Check sign of given number
            let sign = (number >= 0) ? 1 : -1;

            // Set positive value of number of sign negative
            number = number * sign;

            // Separate the int from the decimal part
            let hour = Math.floor(number);
            let decPart = number - hour;

            if (format === 9 && hour.length < 2) {
                hour = '0' + hour;
            }

            let min = 1 / 60;
            // Round to nearest minute
            decPart = min * Math.round(decPart / min);

            let minute = Math.floor(decPart * 60) + '';

            // Add padding if need
            if (minute.length < 2) {
                minute = '0' + minute;
            }

            // Add Sign in final result
            if (format === 0 || format === 9) {
                sign = sign === 1 ? '' : '-';
            } else {
                // Ignore sign when number === 0
                let plusSign = number !== 0. ? '+' : '';
                sign = sign === 1 ? plusSign : '-';
            }

            // Concat hours and minutes
            let newTime;
            if (format === 0 || format === 1 || format === 9) {
                newTime = sign + hour + ':' + minute;
            } else if (format === 2) {
                newTime = sign + ' ' + hour + ':' + minute;
            } else if (format === 3 || format === 4 || format === 7 || format === 8) {
                if (minute > 0 || format === 7 || format === 8) {
                    if ((format === 4 || format === 8) && sign === "+") {
                        newTime = hour + 'h' + minute;
                    } else {
                        newTime = sign + ' ' + hour + 'h' + minute;
                    }
                } else {
                    if (format === 4 && sign === "+") {
                        newTime = hour + 'h';
                    } else {
                        newTime = sign + ' ' + hour + 'h';
                    }
                }
            } else if (format === 5 || format === 6) {
                let hour_str = _t("heure");
                if (hour > 1) {
                    hour_str += 's';
                }
                if (minute > 0) {
                    if (format === 6 && sign === "+") {
                        newTime = hour + ' ' + hour_str + ' ' + minute;
                    } else {
                        newTime = sign + ' ' + hour + ' ' + hour_str + ' ' + minute;
                    }
                } else {
                    if (format === 6 && sign === "+") {
                        newTime = hour + ' ' + hour_str;
                    } else {
                        newTime = sign + ' ' + hour + ' ' + hour_str;
                    }
                }
            }

            return newTime;
        }

        $scope.update_personal_data = function () {
            // Time management
            // + 15:30 // format 2
            // + 15h // format 3
            // 15h // format 4
            // + 15 heure 30 // format 5
            // 15 heure 30 // format 6
            // + 15h30 // format 7
            let time_bank = $scope.personal.actual_bank_hours;
            $scope.personal.actual_bank_sign = (time_bank >= 0);
            $scope.personal.actual_bank_time_diff = $scope.convertNumToTime(time_bank, 2);
            $scope.personal.actual_bank_time_human_short = $scope.convertNumToTime(time_bank, 3);
            $scope.personal.actual_bank_time_human = $scope.convertNumToTime(time_bank, 5);
            $scope.personal.actual_bank_time_human_simplify = $scope.convertNumToTime(time_bank, 6);

            $scope.personal.actual_month_bank_time_human_short = $scope.convertNumToTime($scope.personal.actual_month_bank_hours, 4);

            $scope.personal.nb_echange_en_cours = Object.values($scope.personal.dct_echange).filter(ex => !ex.transaction_valide && moment().isAfter(ex.date) && moment().isBefore(ex.end_date)).length;
            $scope.personal.nb_echange_a_venir = Object.values($scope.personal.dct_echange).filter(ex => !ex.transaction_valide && moment().isBefore(ex.date)).length
            $scope.personal.nb_echange_passe = Object.values($scope.personal.dct_echange).filter(ex => !ex.transaction_valide && moment().isAfter(ex.date)).length

            let month_key = moment(Date.now()).format("MMMM YYYY");
            $scope.personal.dct_echange_mensuel = {};
            $scope.personal.dct_echange_mensuel[month_key] = {
                "lst_echange": [],
                "actualMonth": true,
                "containTransactionValide": false
            };

            // Order list by month and year
            for (const [key, value] of Object.entries($scope.personal.dct_echange)) {
                let inner_obj;
                let month_key = moment(value.date).format("MMMM YYYY");
                if ($scope.personal.dct_echange_mensuel.hasOwnProperty(month_key)) {
                    inner_obj = $scope.personal.dct_echange_mensuel[month_key];
                } else {
                    inner_obj = {"lst_echange": [], "actualMonth": false, "containTransactionValide": false};
                    $scope.personal.dct_echange_mensuel[month_key] = inner_obj;
                }

                if (value.transaction_valide) {
                    inner_obj.containTransactionValide = true;
                }

                value.show_date = moment(value.date).format("dddd D MMMM");
                value.show_start_time = moment(value.date).format("H") + "h" + moment(value.date).format("mm");
                value.show_end_time = moment(value.end_date).format("H") + "h" + moment(value.end_date).format("mm");

                let sign = value.estAcheteur ? -1 : 1;
                value.show_duree_estime = $scope.convertNumToTime(value.duree_estime * sign, 7);
                value.show_duree = $scope.convertNumToTime(value.duree * sign, 7);
                value.show_duree_total_estime = $scope.convertNumToTime((value.duree_estime + value.duree_trajet_estime) * sign, 7);
                value.show_duree_total = $scope.convertNumToTime((value.duree + value.duree_trajet) * sign, 7);
                value.sign = sign;

                inner_obj.lst_echange.push(value);
            }
            for (const [key, value] of Object.entries($scope.personal.dct_echange_mensuel)) {
                // TODO detect if its this month
                value.sum_time = 0;
                for (let i = 0; i < value.lst_echange.length; i++) {
                    let i_echange = value.lst_echange[i];
                    if (i_echange.transaction_valide) {
                        // let duration = i_echange.transaction_valide ? i_echange.duree : i_echange.duree_estime;
                        let duration = i_echange.duree + i_echange.duree_trajet;
                        if (i_echange.estAcheteur) {
                            value.sum_time -= duration;
                        } else {
                            value.sum_time += duration;
                        }
                    }
                }
                value.show_sum_time = $scope.convertNumToTime(value.sum_time, 3);
            }
            console.debug($scope.personal.dct_echange_mensuel);
        }

        $scope.echange_click_redirect = function (echange) {
            // TODO no need this, use instead <a href and not ng-click
            window.location.href = `/monactivite/echange${$scope.url_debug}#!?echange=${echange.id}`;
        }

        $scope.removeSpace = function () {
            let nodeList = document.querySelectorAll(".remove_space");
            for (let i = 0; i < nodeList.length; i++) {
                let nodes = nodeList[i].childNodes;
                for (let j = 0; j < nodes.length; j++) {
                    if (nodes[j].nodeType === Node.TEXT_NODE) {
                        nodes[j].textContent = nodes[j].textContent.trim();
                    }
                }
            }
        };

        $scope.get_list_langue = function () {
            ajax.jsonRpc("/get_available_languages", "call", {}).then(function (response) {
                $scope.language.list = response;
                for (const i in response) {
                    let lang = response[i];
                    if (lang.default) {
                        $scope.language.selected = lang;
                    }
                }
                $scope.$digest();
            }).fail(function (error, ev) {
                console.error(error);
                $scope.check_need_login(error);
            })
        };

        $scope.changeLanguage = function () {
            if ($scope.language.selected.default) {
                console.debug("Ignore update language.");
                return;
            }
            ajax.jsonRpc("/change_language", "call", {lang_code: $scope.language.selected.code}).then(
                function (response) {
                    // window.location.href = `/website/lang/${$scope.language.selected.code}`;
                    // TODO rewrite actual url and not hardcode /monprofil/mespreferences
                    // TODO caution, other language is /en_CA/monprofil/mespreferences
                    window.location.href = "/" + $scope.language.selected.code + `/monprofil/mespreferences${$scope.url_debug}`;
                }).fail(function (error, ev) {
                    console.log(error);
                }
            )
        };
    }])

    let OREAngularJSGlobal = Widget.extend({
        start: function () {
        },
    });

    return OREAngularJSGlobal;

});
