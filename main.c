
#include <stdio.h>
#include <stdlib.h>

#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>


int main(int argc, char **argv)
{
    int ret;
    double res_main;

    // Setup lua interpreter
    lua_State *L;
    L = luaL_newstate();
    luaL_openlibs(L);

    ret = luaL_dofile(L, "script.lua");
    if (ret) {
        fprintf(stderr, "Couldn't load file: %s\n", lua_tostring(L, -1));
        exit(1);
    }

    // Setup env
    lua_createtable(L, 0, 5);

    lua_pushstring(L, "t");
    lua_pushnumber(L, 23.42);
    lua_settable(L, -3);

    lua_pushstring(L, "h");
    lua_pushnumber(L, 1);
    lua_settable(L, -3);

    lua_pushstring(L, "v");
    lua_pushnumber(L, 3);
    lua_settable(L, -3);

    lua_pushstring(L, "h_res");
    lua_pushnumber(L, 1);
    lua_settable(L, -3);

    lua_pushstring(L, "v_res");
    lua_pushnumber(L, 13);
    lua_settable(L, -3);

    lua_setglobal(L, "state");

    // call main
    lua_getglobal(L, "main");

    // 0 args, 1 res, errfunc 0
    if (lua_pcall(L, 0, 1, 0) != 0) {
        fprintf(stderr, "ERROR: %s", lua_tostring(L, -1));
    }

    // get result
    lua_pushnil(L);
    while (lua_next(L, -2) != 0) {
        printf("%s - %s\n",
            lua_typename(L, lua_type(L, -2)),
            lua_typename(L, lua_type(L, -1)));

        printf("rgbw: %.2f\n",
            lua_tonumber(L, -1));
        /* removes 'value'; keeps 'key' for next iteration */
        lua_pop(L, 1);
    }


    lua_close(L);

    return 0;
}

