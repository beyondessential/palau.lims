import SampleTypeContainerController from "./components/sampletype_container.js"
import SampleViewLayoutController from "./components/sampleview_layout.js"


document.addEventListener("DOMContentLoaded", () => {
  console.debug("*** PALAU LIMS JS LOADED ***");

  // Initialize controllers
  window.sampletype_container = new SampleTypeContainerController();
  window.sampleview_layout = new SampleViewLayoutController();

});
