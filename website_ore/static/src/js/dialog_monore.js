odoo.define('website.ore.dialog_monore', function (require) {
    "use strict";

    var ajax = require("web.ajax");
    var core = require('web.core');
    var _t = core._t;
    var Dialog = require('web.Dialog');

    var result = $.Deferred(),
        _templates_loaded = ajax.loadXML(
            "/website_ore/static/src/xml/widgets.xml",
            core.qweb
        );


    var OREForm = Dialog.extend({
        template: "ore.OREForm",

        /**
         * Store models info before creating widget
         *
         * @param {Object} parent Widget where this dialog is attached
         * @param {Object} options Dialog creation options
         * @returns {Dialog} New Dialog object
         */
        init: function (parent, options) {

            var _options = $.extend({}, {
                title: _t("Mon ore"),
                size: "large",
                dialogClass: "modal_ore",
                buttons: [{
                    text: _t("Annuler"),
                    close: true,
                    classes: 'btn-primary btn_ore'
                    },
                    {
                        text: _t("Enregistrer"),
                        close: true,
                        classes: 'btn-primary btn_ore save'
                    }]
            }, options);
            return this._super(parent, _options);
        },

        /**
         * Save data
         */
        save: function () {
            this.final_data = this.$("#model").val();
            console.log("save: " + this.final_data);


            this._super.apply(this, arguments);
        },
    });


    _templates_loaded.done(function () {
        result.resolve({
            OREForm: OREForm,
        });
    });

    $(document).on("click", '.profile_btn.ore', function (ev) {
        let optionsDialog = new OREForm(
            $(".ore_dialog"), {}
        );
        console.log(typeof optionsDialog);
        console.log(optionsDialog);
        //
        // let container = document.getElementsByClassName("ore_dialog");
        // container[0].appendChild(optionsDialog);
        $(".ore_dialog").append(optionsDialog);

        optionsDialog.open();


    })

});
