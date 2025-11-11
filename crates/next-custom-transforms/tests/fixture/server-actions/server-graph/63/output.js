/* __next_internal_action_entry_do_not_use__ {"803128060c414d59f8552e4788b846c0d2b7f74743":"$$RSC_SERVER_CACHE_0"} */ import { registerServerReference } from "private-next-rsc-server-reference";
import { encryptActionBoundArgs, decryptActionBoundArgs } from "private-next-rsc-action-encryption";
import { cache as $$cache__ } from "private-next-rsc-cache-wrapper";
import { cache as $$reactCache__ } from "react";
// @ts-ignore
import { getCachedStuff, wrap } from './foo';
const $$RSC_SERVER_CACHE_0_INNER = async function getCachedData() {
    // This one already worked before.
    return getCachedStuff();
};
export var $$RSC_SERVER_CACHE_0 = $$reactCache__(function getCachedData() {
    return $$cache__("default", "803128060c414d59f8552e4788b846c0d2b7f74743", 0, $$RSC_SERVER_CACHE_0_INNER, arguments);
});
registerServerReference($$RSC_SERVER_CACHE_0, "803128060c414d59f8552e4788b846c0d2b7f74743", null);
Object["defineProperty"]($$RSC_SERVER_CACHE_0, "name", {
    value: "getCachedData"
});
// @ts-ignore
// export { getData } from './data'
export const getCachedData = $$RSC_SERVER_CACHE_0;
export const aliased = getCachedStuff;
const Layout = wrap(async ()=><div>Layout</div>);
const Other = wrap(async ()=><div>Other</div>);
export const Sync = wrap(()=><div>Sync</div>);
export const wrapped = wrap(async ()=>'foo', async ()=>'bar', async ()=>async ()=>'baz', ()=>'sync');
export default Layout;
export { Other, getCachedStuff };
