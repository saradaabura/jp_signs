local modname = minetest.get_current_modname()

-- 1. 文字をUnicode番号(16進数)に変換する関数
-- これにより「あ」と「ぁ」、「A」と「a」を確実に区別して画像を読み込みます
local function char_to_hex(char)
    local cp = 0
    local b1 = string.byte(char, 1)
    if not b1 then return nil end
    
    if b1 < 128 then cp = b1
    elseif b1 < 224 then
        local b2 = string.byte(char, 2)
        cp = (b1 - 192) * 64 + (b2 - 128)
    elseif b1 < 240 then
        local b2 = string.byte(char, 2)
        local b3 = string.byte(char, 3)
        cp = (b1 - 224) * 4096 + (b2 - 128) * 64 + (b3 - 128)
    end
    return string.format("%x", cp)
end

-- 2. UTF-8文字列を分解する関数
local function utf8_to_table(str)
    local t = {}
    if not str then return t end
    for char in str:gmatch("[%z\1-\127\194-\244][\128-\191]*") do
        table.insert(t, char)
    end
    return t
end

-- 3. テクスチャ合成コマンドを生成する関数
local function generate_texture_string(text)
    if not text or text == "" then return "blank.png" end
    
    local chars = utf8_to_table(text)
    local texture_command = "[combine:128x128"
    local x, y = 0, 0
    local has_char = false

    for _, char in ipairs(chars) do
        local hex = char_to_hex(char)
        if hex then
            -- Pythonで生成した Unicode番号のファイル名を参照
            local char_img = "jp_f_" .. hex .. ".png"
            texture_command = texture_command .. ":" .. x .. "," .. y .. "=" .. char_img
            has_char = true
        end

        -- 1文字16pxで配置
        x = x + 16
        if x > 112 then
            x = 0
            y = y + 16
        end
        if y > 112 then break end
    end
    return has_char and texture_command or "blank.png"
end

-- 4. 文字表示用エンティティの登録
minetest.register_entity("jp_signs:text_entity", {
    visual = "upright_sprite",
    textures = {"blank.png"},
    visual_size = {x=1, y=1, z=1},
    physical = false,
    pointable = false,
    static_save = true,
    on_activate = function(self, staticdata)
        if staticdata ~= "" then
            self.object:set_properties({textures = {staticdata}})
        end
    end,
    get_staticdata = function(self)
        return self.object:get_properties().textures[1]
    end,
})

-- 5. 看板ノードの登録
minetest.register_node("jp_signs:board", {
    description = "日本語対応看板 (最終調整版)",
    drawtype = "nodebox",
    tiles = {"default_wood.png"},
    paramtype = "light",
    paramtype2 = "facedir",
    node_box = {
        type = "fixed",
        -- ★板の厚みを調整。背面(0.5)から前面(0.4)まで広げて厚みを出しました
        fixed = {-0.5, -0.5, 0.4, 0.5, 0.5, 0.5},
    },
    groups = {choppy = 2, dig_immediate = 2},

    on_construct = function(pos)
        local meta = minetest.get_meta(pos)
        meta:set_string("formspec", "size[4,2.5]field[0.5,1;3,1;text;表示する文字;]button_exit[1,1.8;2,1;ok;確定]")
    end,

    on_receive_fields = function(pos, formname, fields, sender)
        if fields.ok or fields.key_enter then
            local text = fields.text or ""
            local texture = generate_texture_string(text)
            
            -- 古いエンティティを掃除
            local objects = minetest.get_objects_inside_radius(pos, 0.5)
            for _, obj in ipairs(objects) do
                local ent = obj:get_luaentity()
                if ent and ent.name == "jp_signs:text_entity" then
                    obj:remove()
                end
            end

            -- 向きと位置の計算
            local node = minetest.get_node(pos)
            local dir = minetest.facedir_to_dir(node.param2)
            
            -- ★設置した方向に合わせて表示面を反転
            -- 板の前面(0.4)に対して、0.395 の位置（わずか0.005手前）に配置
            local offset = 0.395
            local ent_pos = {
                x = pos.x + dir.x * offset,
                y = pos.y,
                z = pos.z + dir.z * offset
            }
            
            local obj = minetest.add_entity(ent_pos, "jp_signs:text_entity", texture)
            if obj then
                -- エンティティの向きを看板の正面に合わせる
                obj:set_yaw(minetest.dir_to_yaw(dir))
            end
            
            minetest.get_meta(pos):set_string("infotext", "「" .. text .. "」")
        end
    end,

    -- 壊したときに文字も消す
    after_destruct = function(pos, oldnode)
        local objects = minetest.get_objects_inside_radius(pos, 0.5)
        for _, obj in ipairs(objects) do
            local ent = obj:get_luaentity()
            if ent and ent.name == "jp_signs:text_entity" then
                obj:remove()
            end
        end
    end,
})