/** Resolve the real Add-ons shell through its asynchronous bootstrap states. */
export async function openMolecularPanel(page,panel){
  const tab=page.locator('[data-molsysviewer-addon-workspace-tab="molsysmt"]');
  await tab.waitFor({state:'attached'});
  const toggle=page.getByTitle('Panel mode (N / W)',{exact:true});
  if(!await tab.isVisible()&&await toggle.count()){
    const hot=page.getByRole('button',{name:'Show canvas controls',exact:true});
    await hot.focus();await page.keyboard.press('Enter');await toggle.click();
  }
  // The host can finish selecting Add-ons while click is waiting for layout.
  // Follow the same semantic header in its current or selectable form.
  if(!await tab.isVisible())await page.locator('[data-molsysviewer-panel-stack-option="addons"], [data-molsysviewer-panel-stack-current="addons"]').click();
  await tab.waitFor({state:'visible'});await tab.click();
  await page.locator(`[data-molsysviewer-addon-panel-tab="${panel}"]`).click();
  await page.locator(`.msm-${panel}`).waitFor();
}
