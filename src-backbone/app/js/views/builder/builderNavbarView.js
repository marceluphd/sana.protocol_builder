let Helpers = require('utils/helpers');
let App     = require('utils/sanaAppInstance');


module.exports = Marionette.ItemView.extend({

    template: require('templates/builder/builderNavbarView'),

    tagName: 'div',

    className: 'container-fluid spb-container',

    ui: {
        statusText: 'p.status-text'
    },

    //-------------------------------------------------------------------------
    // File menu
    //-------------------------------------------------------------------------

    events: {
        'click #menu-bar ul.file a.save'  : '_onFileSave',
        'click #menu-bar ul.file a.delete': '_onFileDelete',
    },

    _onFileSave: function() {
        this.model.save();
    },

    _onFileDelete: function() {
        // TODO prompt user for confirmation

        let self = this;
        this.model.destroy({
            success: function() {
                console.info('Deleted Procedure', self.model.get('id'));
                Helpers.navigateToDefaultLoggedIn();
            },
            error: function() {
                console.warn('Failed to delete Procedure', self.model.get('id'));
                App().showNotification('danger', 'Failed delete Procedure!');
            },
        });
    },

    //-------------------------------------------------------------------------
    // Model events
    //-------------------------------------------------------------------------

    initialize: function() {
        this.listenTo(this.model, 'request', this.saving); // Whenenever an AJAX call is made
        this.listenTo(this.model, 'sync', this.saved); // After server responds
        this.listenTo(this.model, 'destroy', this.saved); // After server responds
        this.listenTo(this.model, 'error', this.error); // After server responds with error
    },

    saving: function (event) {
        this.ui.statusText.text('Saving...');
    },

    saved: function(event) {
        this.ui.statusText.text('All changes saved to server.');
    },

    error: function(event) {
        this.ui.statusText.text('Failed to synchronize with server. Please try again.');
    },

});
