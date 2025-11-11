/* __next_internal_action_entry_do_not_use__ {"803128060c414d59f8552e4788b846c0d2b7f74743":"$$RSC_SERVER_CACHE_0","ff1acff246876a467753785a92d1f95ac6fe32c9b9":"Other","ff27fadf3eeb97c777cea9f14a407b5c0b42ac65bb":"aliased","ff438bb59117ff1af890c80ca3e39d9e888fc93033":"wrapped","ff7f03edbc83b6cc7e5ccc12da8fecf25146585bb7":"getCachedData","ff84effee663e5ce4e0948b55df129a8df904c67aa":"Sync","ff85cca0cc8341c33fcca0288c72a60d67cbda2eee":"getCachedStuff","ffc18c215a6b7cdc64bf709f3a714ffdef1bf9651d":"default"} */ import { registerServerReference } from "private-next-rsc-server-reference";
import { encryptActionBoundArgs, decryptActionBoundArgs } from "private-next-rsc-action-encryption";
import { cache as $$cache__ } from "private-next-rsc-cache-wrapper";
import { cache as $$reactCache__ } from "react";
// @ts-ignore
import { getCachedStuff as $$RSC_SERVER_CACHE_1_ORIG, wrap } from './foo';
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
;
let aliased = $$RSC_SERVER_CACHE_1_ORIG;
if (typeof $$RSC_SERVER_CACHE_1_ORIG === "function") {
    aliased = $$reactCache__(function aliased() {
        return $$cache__("default", "ff27fadf3eeb97c777cea9f14a407b5c0b42ac65bb", 0, $$RSC_SERVER_CACHE_1_ORIG, arguments);
    });
    registerServerReference(aliased, "ff27fadf3eeb97c777cea9f14a407b5c0b42ac65bb", null);
    Object["defineProperty"](aliased, "name", {
        value: "aliased"
    });
}
export { aliased };
const $$RSC_SERVER_CACHE_2_ORIG = wrap(async ()=><div>Layout</div>);
const $$RSC_SERVER_CACHE_3_ORIG = wrap(async ()=><div>Other</div>);
;
const $$RSC_SERVER_CACHE_4_ORIG = wrap(()=><div>Sync</div>);
let Sync = $$RSC_SERVER_CACHE_4_ORIG;
if (typeof $$RSC_SERVER_CACHE_4_ORIG === "function") {
    Sync = $$reactCache__(function Sync() {
        return $$cache__("default", "ff84effee663e5ce4e0948b55df129a8df904c67aa", 0, $$RSC_SERVER_CACHE_4_ORIG, arguments);
    });
    registerServerReference(Sync, "ff84effee663e5ce4e0948b55df129a8df904c67aa", null);
    Object["defineProperty"](Sync, "name", {
        value: "Sync"
    });
}
export { Sync };
;
const $$RSC_SERVER_CACHE_5_ORIG = wrap(async ()=>'foo', async ()=>'bar', async ()=>async ()=>'baz', ()=>'sync');
let wrapped = $$RSC_SERVER_CACHE_5_ORIG;
if (typeof $$RSC_SERVER_CACHE_5_ORIG === "function") {
    wrapped = $$reactCache__(function wrapped() {
        return $$cache__("default", "ff438bb59117ff1af890c80ca3e39d9e888fc93033", 0, $$RSC_SERVER_CACHE_5_ORIG, arguments);
    });
    registerServerReference(wrapped, "ff438bb59117ff1af890c80ca3e39d9e888fc93033", null);
    Object["defineProperty"](wrapped, "name", {
        value: "wrapped"
    });
}
export { wrapped };
;
let Layout = $$RSC_SERVER_CACHE_2_ORIG;
if (typeof $$RSC_SERVER_CACHE_2_ORIG === "function") {
    Layout = $$reactCache__(function() {
        return $$cache__("default", "ffc18c215a6b7cdc64bf709f3a714ffdef1bf9651d", 0, $$RSC_SERVER_CACHE_2_ORIG, arguments);
    });
    registerServerReference(Layout, "ffc18c215a6b7cdc64bf709f3a714ffdef1bf9651d", null);
    Object["defineProperty"](Layout, "name", {
        value: "default"
    });
}
export default Layout;
;
let Other = $$RSC_SERVER_CACHE_3_ORIG;
if (typeof $$RSC_SERVER_CACHE_3_ORIG === "function") {
    Other = $$reactCache__(function Other() {
        return $$cache__("default", "ff1acff246876a467753785a92d1f95ac6fe32c9b9", 0, $$RSC_SERVER_CACHE_3_ORIG, arguments);
    });
    registerServerReference(Other, "ff1acff246876a467753785a92d1f95ac6fe32c9b9", null);
    Object["defineProperty"](Other, "name", {
        value: "Other"
    });
}
;
let getCachedStuff = $$RSC_SERVER_CACHE_1_ORIG;
if (typeof $$RSC_SERVER_CACHE_1_ORIG === "function") {
    getCachedStuff = $$reactCache__(function getCachedStuff() {
        return $$cache__("default", "ff85cca0cc8341c33fcca0288c72a60d67cbda2eee", 0, $$RSC_SERVER_CACHE_1_ORIG, arguments);
    });
    registerServerReference(getCachedStuff, "ff85cca0cc8341c33fcca0288c72a60d67cbda2eee", null);
    Object["defineProperty"](getCachedStuff, "name", {
        value: "getCachedStuff"
    });
}
export { Other, getCachedStuff };
