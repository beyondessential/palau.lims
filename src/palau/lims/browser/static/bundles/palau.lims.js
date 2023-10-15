(()=>{"use strict";var t={311:t=>{t.exports=jQuery}},e={};function i(n){var o=e[n];if(void 0!==o)return o.exports;var r=e[n]={exports:{}};return t[n](r,r.exports,i),r.exports}(()=>{var t=i(311);function e(t){return e="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},e(t)}function n(t,i){for(var n=0;n<i.length;n++){var o=i[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(t,(void 0,r=function(t,i){if("object"!==e(t)||null===t)return t;var n=t[Symbol.toPrimitive];if(void 0!==n){var o=n.call(t,"string");if("object"!==e(o))return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return String(t)}(o.key),"symbol"===e(r)?r:String(r)),o)}var r}var o=[].indexOf;const r=function(){function e(){var i,n,r,l;if(function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,e),this.is_required=this.is_required.bind(this),this.bind_event_handler=this.bind_event_handler.bind(this),this.on_template_selected=this.on_template_selected.bind(this),this.on_bottle_weight_change=this.on_bottle_weight_change.bind(this),this.on_bottle_container_blur=this.on_bottle_container_blur.bind(this),this.on_sample_type_selected=this.on_sample_type_selected.bind(this),this.get_sample_index=this.get_sample_index.bind(this),this.update_container=this.update_container.bind(this),this.toggle_container_visibility=this.toggle_container_visibility.bind(this),this.set_volume_readonly=this.set_volume_readonly.bind(this),this.calculate_volume=this.calculate_volume.bind(this),this.get_float_value=this.get_float_value.bind(this),this.round=this.round.bind(this),this.set_visible=this.set_visible.bind(this),this.fetch=this.fetch.bind(this),this.ajax_submit=this.ajax_submit.bind(this),this.get_portal_url=this.get_portal_url.bind(this),this.debug=this.debug.bind(this),this.get_add_controller=this.get_add_controller.bind(this),this.is_required()){if(this.debug("load"),this.sample_type_selector="div.uidreferencefield textarea[name^='SampleType']",this.template_selector="input[id^='Template']",this.bottle_weights_selector="input[id^='Bottles-'][id*='-Weight-']",this.bottle_containers_selector="input[id^='Bottles-'][id*='-Container-']",this.bind_event_handler(),o.call(document.body.classList,"template-ar_add")>=0)for(n=0,r=(l=document.querySelectorAll(this.sample_type_selector)).length;n<r;n++)i=l[n],t(i).trigger("select");else document.querySelector("div[data-fieldname='Bottles']")&&(i=document.querySelector("input[id='Volume']")).setAttribute("readonly","readonly");return this}}var i,r;return i=e,r=[{key:"is_required",value:function(){var t,e,i,n,o,r;for(r=["template-ar_add","portaltype-analysisrequest"],e=i=0,n=(o=document.body.classList).length;i<n;e=++i)if(t=o[e],r.includes(t))return!0;return!1}},{key:"bind_event_handler",value:function(){return this.debug("bind_event_handler"),t("body").on("SampleType:after_change",this.sample_type_selector,this.on_sample_type_selected),t("body").on("selected",this.template_selector,this.on_template_selected),t("body").on("blur",this.bottle_containers_selector,this.on_bottle_container_blur),t("body").on("change",this.bottle_weights_selector,this.on_bottle_weight_change)}},{key:"on_template_selected",value:function(e){var i,n,o;if(this.debug("on_template_selected"),i=e.currentTarget,n=this.get_sample_index(i),o=t("#".concat(i.id)).attr("uid"))return this.fetch(o,[]).done((function(t){var e;if(t)return e=t.SampleType_uid,this.update_container(n,e)}))}},{key:"on_bottle_weight_change",value:function(t){var e,i;return this.debug("on_bottle_weight_change"),e=t.currentTarget,i=this.get_sample_index(e),this.calculate_volume(i)}},{key:"on_bottle_container_blur",value:function(t){var e,i;return this.debug("on_bottle_container_blur"),e=t.currentTarget,i=this.get_sample_index(e),this.calculate_volume(i)}},{key:"on_sample_type_selected",value:function(t){var e,i;return this.debug("on_sample_type_selected"),e=t.currentTarget,i=this.get_sample_index(e),this.update_container(i,e.value)}},{key:"get_sample_index",value:function(e){var i;return this.debug("get_sample_index:element=".concat(e.id)),(i=e.closest("td[arnum]"))?t(i).attr("arnum"):null}},{key:"update_container",value:function(t,e){var i;return this.debug("update_container:sample_index=".concat(t,",sample_type_uid=").concat(e)),e?(i="ContainerWidget",this.fetch(e,i).done((function(e){var n;if(n=!1,e&&(n="container"===e[i]),this.toggle_container_visibility(t,n),this.set_volume_readonly(t,!n),!n)return this.calculate_volume(t)}))):(this.toggle_container_visibility(t,!0),this.set_volume_readonly(t,!1))}},{key:"toggle_container_visibility",value:function(t,e){return this.debug("toggle_container_visibility:sample_index=".concat(t,",show_container=").concat(e)),this.set_visible("Container",t,e),this.set_visible("Bottles",t,!e)}},{key:"set_volume_readonly",value:function(t,e){var i,n;if(this.debug("set_volume_readonly:sample_index=".concat(t,",readonly=").concat(e)),n="#Volume",t&&(n="#Volume-".concat(t)),i=document.querySelector(n))return e?i.setAttribute("readonly","readonly"):i.removeAttribute("readonly")}},{key:"calculate_volume",value:function(e){var i,n,o,r,l,s;if(this.debug("calculate_volume:sample_index=".concat(e)),r=0,n="tr.records_row_Bottles",e&&(n="tr.records_row_Bottles-".concat(e)),i=document.querySelectorAll(n),o=this,t.each(i,(function(t,i){var n,l,s,a,u,c;return c="#Bottles-Weight-".concat(t),e&&(c="#Bottles-".concat(e,"-Weight-").concat(t)),u=i.querySelector(c),u=o.get_float_value(u),o.debug("Not a valid volume: ".concat(u)),l="#Bottles-DryWeight-".concat(t),e&&(l="#Bottles-".concat(e,"-DryWeight-").concat(t)),n=i.querySelector(l),n=o.get_float_value(n),o.debug("Not a valid volume: ".concat(n)),(s=u-n)<=0?(o.debug("Not a valid bottle volume: ".concat(s)),s=""):(s=o.round(1.05*s,3),r+=s),a="#Bottles-Volume-".concat(t),e&&(a="#Bottles-".concat(e,"-Volume-").concat(t)),i.querySelector(a).value=s})),r=parseFloat(r),(r=this.round(r,4))<=0?(this.debug("Not a valid volume: ".concat(r)),r=""):r+=" ml",s="#Volume",e&&(s="#Volume-".concat(e)),l=document.querySelector(s))return l.value=r}},{key:"get_float_value",value:function(t){var e,i=arguments.length>1&&void 0!==arguments[1]?arguments[1]:0;return e=parseFloat(t.value),isNaN(e)&&(e=parseFloat(i)),e}},{key:"round",value:function(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:2;return Number(Math.round(t+"e"+e)+"e-"+e)}},{key:"set_visible",value:function(e,i,n){var o,r;return this.debug("set_visible:field_name=".concat(e,",sample_index=").concat(i,",visible=").concat(n)),r="div[data-fieldname='".concat(e,"']"),i&&(r="div[data-fieldname='".concat(e,"-").concat(i,"']")),"0"===i&&"1"===document.querySelector("#ar_count").value&&(r="tr[fieldname=".concat(e,"]")),o=document.querySelector(r),n?t(o).show():t(o).hide()}},{key:"fetch",value:function(e,i){var n,o;return this.debug("fetch:uid=".concat(e,",field_names=").concat(i)),n=t.Deferred(),o={url:this.get_portal_url()+"/@@API/read",data:{catalog_name:"senaite_catalog_setup",UID:e,include_fields:i,page_size:1}},this.ajax_submit(o).done((function(t){var e;return e={},t.objects&&(e=t.objects[0]),n.resolveWith(this,[e])})),n.promise()}},{key:"ajax_submit",value:function(){var e,i=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return this.debug("ajax_submit"),null==i.type&&(i.type="POST"),null==i.url&&(i.url=this.get_portal_url()),null==i.context&&(i.context=this),null==i.dataType&&(i.dataType="json"),null==i.data&&(i.data={}),null==i._authenticator&&(i._authenticator=t("input[name='_authenticator']").val()),this.debug(">>> ajax_submit::options=",i),t(this).trigger("ajax:submit:start"),e=function(){return t(this).trigger("ajax:submit:end")},t.ajax(i).done(e)}},{key:"get_portal_url",value:function(){return t("input[name=portal_url]").val()||window.portal_url}},{key:"debug",value:function(t){}},{key:"get_add_controller",value:function(){return window.bika.lims.AnalysisRequestAdd}}],r&&n(i.prototype,r),Object.defineProperty(i,"prototype",{writable:!1}),e}();var l=i(311),s=function(t,e){return function(){return t.apply(e,arguments)}};const a=function(){function t(){var t,e,i,n;if(this.debug=s(this.debug,this),this.init_sections_visibility=s(this.init_sections_visibility,this),this.init_toggle=s(this.init_toggle,this),this.on_toggle_selector_clicked=s(this.on_toggle_selector_clicked,this),this.is_required=s(this.is_required,this),this.is_required()){for(this.debug("load"),t=0,e=(n=[["#content h1","#senaite-sampleheader","png-lims-sample-header"],["#content h1","div[id=ar-attachments]","png-lims-sample-header"],["div.remarks-widget h3","div.remarks-widget div","png-lims-sample-remarks-section"],["div.analysis-listing-table h3","div.analysis-listing-table form","png-lims-sample-analyses-section"],["div[id=results-interpretation] h3","div[id=results-interpretation] form","png-lims-sample-results-interpretation-section"]]).length;t<e;t++)i=n[t],this.init_toggle(i[0],i[1],i[2]);return l("body").on("click",".toggle_selector",this.on_toggle_selector_clicked),this.init_sections_visibility(),this}}return t.prototype.is_required=function(){var t,e,i,n,o,r;for(r=["portaltype-analysisrequest"],e=i=0,n=(o=document.body.classList).length;i<n;e=++i)if(t=o[e],r.includes(t))return!0;return!1},t.prototype.on_toggle_selector_clicked=function(t){var e,i,n,o,r,s;for(this.debug("on_toggle_selector_clicked"),o=t.currentTarget.getAttribute("target-section"),e=0,i=(r=document.querySelectorAll("[section="+o+"]")).length;e<i;e++)n=r[e],(s=this.is_visible(n))?l(n).hide():l(n).show();return site.set_cookie(o,!s)},t.prototype.init_toggle=function(t,e,i){var n;return this.debug("init_toggle:anchor_selector='"+t+"',section_selector='"+e+"',section_id='"+i+"'"),(n=document.querySelector(t)).classList.add("toggle_selector"),n.setAttribute("target-section",i),document.querySelector(e).setAttribute("section",i)},t.prototype.is_visible=function(t){return"none"!==l(t).css("display")},t.prototype.init_sections_visibility=function(){var t,e,i,n,o,r,s,a;for(this.debug("set_visibility"),n=[],e=0,i=(t=document.querySelectorAll(".toggle_selector")).length;e<i;e++)r=t[e].getAttribute("target-section"),a=site.read_cookie(r)||"true",this.debug("section_id="+r+", visible="+a),a="true"===a,s=document.querySelectorAll("[section="+r+"]"),n.push(function(){var t,e,i;for(i=[],t=0,e=s.length;t<e;t++)o=s[t],a?i.push(l(o).show()):i.push(l(o).hide());return i}());return n},t.prototype.debug=function(t){},t}();document.addEventListener("DOMContentLoaded",(function(){window.sampletype_container=new r,window.sampleview_layout=new a}))})()})();