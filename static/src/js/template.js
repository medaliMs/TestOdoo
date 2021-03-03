/*
const { Component } = owl;
const { xml } = owl.tags;
const { whenReady } = owl.utils;

// Owl Components
class App extends Component {
  static template = xml`<div>Hello Owl</div>`;
}

// Setup code
function setup() {
  const app = new App();
  app.mount(document.body);
}

whenReady(setup);

*/
const { Component, useState, tags, mount } = owl;
const { xml, css } = tags;
const { whenReady } = owl.utils;

// Counter component
const COUNTER_TEMPLATE = xml`
  <button t-on-click="state.value++">
    Click! [<t t-esc="state.value"/>]
  </button>`;

const COUNTER_STYLE = css`
  button {
    color: blue;
  }`;

class Counter extends Component {
  state = useState({ value: 0})
}
Counter.template = COUNTER_TEMPLATE;
Counter.style = COUNTER_STYLE;

// App
const APP_TEMPLATE = xml`
  <div>
    <Counter/>
    <Counter/>
  </div>`;

class App extends Component {}
App.template = APP_TEMPLATE;
App.components = { Counter };
function setup() {
  const app = new App();
  app.mount(document.body);
  }
  whenReady(setup);
