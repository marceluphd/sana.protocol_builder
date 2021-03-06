const ChoicesCollectionView = require('views/builder/pageDetails/pageElements/choices/choicesCollectionView');
const Choice = require('models/choice');
const Helpers = require('utils/helpers');


module.exports = Marionette.Behavior.extend({

    events: {
        'keypress input.new-choice': '_onKeyPressNewChoiceInput',
        'paste input.new-choice': '_onPasteNewChoiceInput',
    },

    onBeforeShow: function() {
        this.choicesCollectionView = new ChoicesCollectionView({
            collection: this.view.model.choices,
        });
        
        this.view.showChildView('choicesList', this.choicesCollectionView);
    },

    //--------------------------------------------------------------------------
    // Event handlers
    //--------------------------------------------------------------------------

    _onKeyPressNewChoiceInput: function(event) {
        if (!event.which) {
            // Do nothing when keypress is not a valid character
            return;
        }

        event.preventDefault();

        let newChoice = this.view.model.createNewChoice(String.fromCharCode(event.keyCode));
        this._changeFocusToNewChoice(newChoice);
    },

    _onPasteNewChoiceInput: function(event) {
        event.preventDefault();

        let text = (event.originalEvent || event).clipboardData.getData('text');
        let newChoice = this.view.model.createNewChoice(text);
        this._changeFocusToNewChoice(newChoice);
    },

    //--------------------------------------------------------------------------
    // Helpers
    //--------------------------------------------------------------------------

    _changeFocusToNewChoice: function(newChoice) {
        let choiceView = this.choicesCollectionView.children.findByModel(newChoice);

        // Ensure even if there's no input afterwards, Choice model will still trigger a change event to save
        choiceView.saveChoice();

        let $input = choiceView.$el.find('div.input');
        $input.focus();

        let range = document.createRange();
        range.selectNodeContents($input.get(0));
        range.collapse(false); // Move focus to end of range

        let selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
    },

});
