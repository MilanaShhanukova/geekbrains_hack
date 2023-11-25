import { getGreeting } from '../support/app.po';

describe('hackaton-speech2text-glossary', () => {
  beforeEach(() => cy.visit('/'));

  it('should display welcome message', () => {
    // Custom command example, see `../support/commands.ts` file
    cy.login('my-email@something.com', 'myPassword');

    // Function helper example, see `../support/app.po.ts` file
    getGreeting().contains('Welcome hackaton-speech2text-glossary');
  });
});
