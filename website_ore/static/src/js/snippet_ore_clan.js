odoo.define("ore_clan_list.animation", function (require) {
    "use strict";

    let sAnimation = require("website.content.snippets.animation");

    sAnimation.registry.ore = sAnimation.Class.extend({
        selector: ".o_ore_liste_clan",

        start: function () {
            let self = this;
            this._eventList = this.$(".container");
            this._originalContent = this._eventList[0].outerHTML;
            let def = this._rpc({route: "/ore/ore_clan_list"}).then(function (data) {
                if (data.error) {
                    return;
                }

                if (_.isEmpty(data)) {
                    return;
                }

                self._$loadedContent = $(data[0]);
                self._eventList.replaceWith(self._$loadedContent);

                console.debug(data);

                // Update autocomplete
                let select_item = $('#chooseClan');
                if (select_item.length === 0) {
                    console.error(`Missing ${select_item}`)
                } else {
                    let autoCompleteJS = new autoComplete({
                        selector: "#chooseClan",
                        data: {
                            src: data[1],
                            keys: ["name"],
                            cache: true,
                        },
                        resultItem: {
                            element: (element, data) => {
                                element.innerHTML = `<img style="width:50px; aspect-ratio: 1;" src="${data.value.img}" class="nav_pic rounded-circle"/>${data.match}`
                            },
                            highlight: true,
                        },
                        resultsList: {
                            element: (list, data) => {
                                const message = document.createElement("div");
                                if (!data.results.length) {
                                    // Create "No Results" message list element
                                    message.setAttribute("class", "no_result");
                                    // Add message text content
                                    message.innerHTML = `<span>Aucun résultat trouvé pour &nbsp;"${data.query}"</span>`;
                                } else {
                                    message.innerHTML = `<strong>${data.results.length}</strong>&nbsp; sur &nbsp;<strong>${data.matches.length}</strong> &nbsp; résultats`;
                                }
                                // Add message list element to the list
                                list.prepend(message);
                            },
                            maxResults: 10,
                            noResults: true,
                            highlight: {
                                render: true,
                            },
                        },
                    });
                    autoCompleteJS.input.addEventListener("selection", function (event) {
                      const feedback = event.detail;
                      autoCompleteJS.input.blur();
                      console.log(feedback);
                      console.log(feedback.selection.value);
                      window.location.href = feedback.selection.value.url;
                    });
                }

            });

            return $.when(this._super.apply(this, arguments), def);
        },
        destroy: function () {
            this._super.apply(this, arguments);
            if (this._$loadedContent) {
                this._$loadedContent.replaceWith(this._originalContent);
            }
        },
    });
});
