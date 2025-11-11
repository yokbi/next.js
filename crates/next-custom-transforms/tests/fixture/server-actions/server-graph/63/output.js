/* __next_internal_action_entry_do_not_use__ {"803128060c414d59f8552e4788b846c0d2b7f74743":"$$RSC_SERVER_CACHE_0","ff1acff246876a467753785a92d1f95ac6fe32c9b9":"Other","ff27fadf3eeb97c777cea9f14a407b5c0b42ac65bb":"aliased","ff438bb59117ff1af890c80ca3e39d9e888fc93033":"wrapped","ff84effee663e5ce4e0948b55df129a8df904c67aa":"Sync","ff85cca0cc8341c33fcca0288c72a60d67cbda2eee":"getCachedStuff","ff8fa22f08e492db15701f58a1458cc4ebf782f855":"getData","ffc18c215a6b7cdc64bf709f3a714ffdef1bf9651d":"default"} */ import { registerServerReference } from "private-next-rsc-server-reference";
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
export const getCachedData = $$RSC_SERVER_CACHE_0;
// @ts-ignore
import { getData } from './data';
const aliased = getCachedStuff;
const Layout = wrap(async ()=><div>Layout</div>);
const Other = wrap(async ()=><div>Other</div>);
const Sync = wrap(()=><div>Sync</div>);
const wrapped = wrap(async ()=>'foo', async ()=>'bar', async ()=>async ()=>'baz', ()=>'sync');
let $$RSC_SERVER_CACHE_getData = getData;
if (typeof getData === "function") {
    $$RSC_SERVER_CACHE_getData = $$reactCache__(function getData() {
        return $$cache__("default", "ff8fa22f08e492db15701f58a1458cc4ebf782f855", 0, getData, arguments);
    });
    registerServerReference($$RSC_SERVER_CACHE_getData, "ff8fa22f08e492db15701f58a1458cc4ebf782f855", null);
    Object["defineProperty"]($$RSC_SERVER_CACHE_getData, "name", {
        value: "getData"
    });
}
export { $$RSC_SERVER_CACHE_getData as getData };
let $$RSC_SERVER_CACHE_aliased = aliased;
if (typeof aliased === "function") {
    $$RSC_SERVER_CACHE_aliased = $$reactCache__(function aliased1() {
        return $$cache__("default", "ff27fadf3eeb97c777cea9f14a407b5c0b42ac65bb", 0, aliased, arguments);
    });
    registerServerReference($$RSC_SERVER_CACHE_aliased, "ff27fadf3eeb97c777cea9f14a407b5c0b42ac65bb", null);
    Object["defineProperty"]($$RSC_SERVER_CACHE_aliased, "name", {
        value: "aliased"
    });
}
export { $$RSC_SERVER_CACHE_aliased as aliased };
let $$RSC_SERVER_CACHE_Sync = Sync;
if (typeof Sync === "function") {
    $$RSC_SERVER_CACHE_Sync = $$reactCache__(function Sync1() {
        return $$cache__("default", "ff84effee663e5ce4e0948b55df129a8df904c67aa", 0, Sync, arguments);
    });
    registerServerReference($$RSC_SERVER_CACHE_Sync, "ff84effee663e5ce4e0948b55df129a8df904c67aa", null);
    Object["defineProperty"]($$RSC_SERVER_CACHE_Sync, "name", {
        value: "Sync"
    });
}
export { $$RSC_SERVER_CACHE_Sync as Sync };
let $$RSC_SERVER_CACHE_wrapped = wrapped;
if (typeof wrapped === "function") {
    $$RSC_SERVER_CACHE_wrapped = $$reactCache__(function wrapped1() {
        return $$cache__("default", "ff438bb59117ff1af890c80ca3e39d9e888fc93033", 0, wrapped, arguments);
    });
    registerServerReference($$RSC_SERVER_CACHE_wrapped, "ff438bb59117ff1af890c80ca3e39d9e888fc93033", null);
    Object["defineProperty"]($$RSC_SERVER_CACHE_wrapped, "name", {
        value: "wrapped"
    });
}
export { $$RSC_SERVER_CACHE_wrapped as wrapped };
let $$RSC_SERVER_CACHE_default = Layout;
if (typeof Layout === "function") {
    $$RSC_SERVER_CACHE_default = $$reactCache__(function() {
        return $$cache__("default", "ffc18c215a6b7cdc64bf709f3a714ffdef1bf9651d", 0, Layout, arguments);
    });
    registerServerReference($$RSC_SERVER_CACHE_default, "ffc18c215a6b7cdc64bf709f3a714ffdef1bf9651d", null);
    Object["defineProperty"]($$RSC_SERVER_CACHE_default, "name", {
        value: "default"
    });
}
export default $$RSC_SERVER_CACHE_default;
let $$RSC_SERVER_CACHE_Other = Other;
if (typeof Other === "function") {
    $$RSC_SERVER_CACHE_Other = $$reactCache__(function Other1() {
        return $$cache__("default", "ff1acff246876a467753785a92d1f95ac6fe32c9b9", 0, Other, arguments);
    });
    registerServerReference($$RSC_SERVER_CACHE_Other, "ff1acff246876a467753785a92d1f95ac6fe32c9b9", null);
    Object["defineProperty"]($$RSC_SERVER_CACHE_Other, "name", {
        value: "Other"
    });
}
export { $$RSC_SERVER_CACHE_Other as Other };
let $$RSC_SERVER_CACHE_getCachedStuff = getCachedStuff;
if (typeof getCachedStuff === "function") {
    $$RSC_SERVER_CACHE_getCachedStuff = $$reactCache__(function getCachedStuff1() {
        return $$cache__("default", "ff85cca0cc8341c33fcca0288c72a60d67cbda2eee", 0, getCachedStuff, arguments);
    });
    registerServerReference($$RSC_SERVER_CACHE_getCachedStuff, "ff85cca0cc8341c33fcca0288c72a60d67cbda2eee", null);
    Object["defineProperty"]($$RSC_SERVER_CACHE_getCachedStuff, "name", {
        value: "getCachedStuff"
    });
}
export { $$RSC_SERVER_CACHE_getCachedStuff as getCachedStuff };
