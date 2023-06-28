// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
odoo.define('auth_signup_policy.signup', function (require) {
    'use strict';

    let base = require('web_editor.base');

    base.ready().then(function () {
        // Disable 'Sign Up' if it needs check policy
        let $form = $('.oe_signup_form');
        if ($form.length > 0) {
            if ($('.signup-policy').length > 0) {
                let $btn = $form.find('.oe_login_buttons > button[type="submit"]');
                let $check = $('#accept_global_policy');

                if (!$check.is(':checked')) {
                    $btn.attr('disabled', 'disabled');
                }

                // Disable when checkbox change
                $check.on('change', function () {
                    if ($(this).is(':checked')) {
                        $btn.removeAttr('disabled');
                    } else {
                        $btn.attr('disabled', 'disabled');
                    }
                });
            }
        }
    });
});
