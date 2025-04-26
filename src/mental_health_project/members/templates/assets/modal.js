/**
 * For handling modals
 */

"use strict";

/**
 * Main html modal
 */
class Modal {
    /**
     * Builds the modal
     * @param {String} id Required. The id of the modal
     * @param {String} id_close Required. The id of the button that closes the modal
     */
    constructor(id, id_close) {
        this.id = id;
        this.elm = document.getElementById(id);
        this.bt_close = document.getElementById(id_close);
    }
    /**
     * Shows the modal
     */
    open() {
        this.elm.style.display = "block";
    }
    /**
     * Closes the modal
     */
    close() {
        this.elm.style.display = "none";
    }
}