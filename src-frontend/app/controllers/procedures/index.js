import Ember from 'ember';

export default Ember.Controller.extend({
    actions: {
        createProcedure: function() {
            // TODO: Deal with owner ID and user-inputted information
            var procedureController = this;
            var procedure = this.store.createRecord('procedure', {
                title: 'Surgery Follow-Up',
                author: 'Partners for Care',
                owner: 1
            });

            procedure.save().then(function() {
                procedureController.transitionToRoute('procedure', procedure);
            });
        }
    }
});