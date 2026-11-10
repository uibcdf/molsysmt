/** Resolve the real Add-ons shell through its asynchronous bootstrap states. */
export async function observeMolecularControllers(page){
  // Retain actual runtime objects without changing a command or its result.
  // The same observation route serves ordinary widgets and canvas popups.
  await page.addInitScript(()=>{
    let runtime;window.__controllers=[];
    Object.defineProperty(window,'__molsysviewer_anywidget_runtime__',{configurable:true,get:()=>runtime,set(value){
      runtime=value;const C=value?.module?.MolSysViewerController;if(!C)return;
      const create=C.create;C.create=async function(...args){const c=await create.apply(this,args);window.__controllers.push(c);return c;};
    }});
    const open=window.open.bind(window);
    window.open=(...args)=>{
      const win=open(...args);if(!win)return win;
      const append=win.Node.prototype.appendChild;
      win.Node.prototype.appendChild=function(node){
        if(node.tagName==='SCRIPT'&&node.textContent.includes('await boot(module)'))node.textContent=node.textContent.replace('await boot(module)',`const create=module.MolSysViewerController.create;
          module.MolSysViewerController.create=async function(...args){const c=await create.apply(this,args);window.__controllers=[...(window.__controllers||[]),c];return c;};await boot(module)`);
        return append.call(this,node);
      };
      return win;
    };
  });
}

export async function openMolecularPanel(page,panel,root=page){
  const tab=root.locator('[data-molsysviewer-addon-workspace-tab="molsysmt"]');
  await tab.waitFor({state:'attached'});
  const toggle=root.getByTitle('Panel mode (N / W)',{exact:true});
  if(!await tab.isVisible()&&await toggle.count()){
    const hot=root.getByRole('button',{name:'Show canvas controls',exact:true});
    await hot.focus();await page.keyboard.press('Enter');await toggle.click();
  }
  // The host can finish selecting Add-ons while click is waiting for layout.
  // Follow the same semantic header in its current or selectable form.
  if(!await tab.isVisible())await root.locator('[data-molsysviewer-panel-stack-option="addons"], [data-molsysviewer-panel-stack-current="addons"]').click();
  await tab.waitFor({state:'visible'});await tab.click();
  await root.locator(`[data-molsysviewer-addon-panel-tab="${panel}"]`).click();
  // Geometry reuses System styling and identifies itself with this heading.
  await root.locator(panel==='geometry'?'[data-geometry-heading]':`.msm-${panel}`).waitFor();
}
