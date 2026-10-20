// Phase 05 hair shells (tools/phase05_hair.py): shell k of N keeps the strands taller than its height. The strand
// texture is sampled no blurrier than mip 0.5 so single strands survive at gameplay distance instead of averaging
// into a solid sheet (plain mipmapped alpha-scissor shells collapse into a helmet).
shader_type spatial;
render_mode cull_back, depth_draw_opaque, diffuse_burley, specular_schlick_ggx;

uniform sampler2D strands : source_color, filter_linear_mipmap, repeat_disable;
uniform float shell_height = 0.5;
uniform float tint = 1.0;
uniform float roughness_value = 0.78;

void fragment() {
	vec2 size = vec2(textureSize(strands, 0));
	vec2 dx = dFdx(UV * size);
	vec2 dy = dFdy(UV * size);
	float lod = 0.5 * log2(max(dot(dx, dx), dot(dy, dy)));
	vec4 t = textureLod(strands, UV, clamp(lod - 0.5, 0.0, 0.5));
	ALBEDO = t.rgb * tint;
	ALPHA = t.a;
	ALPHA_SCISSOR_THRESHOLD = shell_height;
	ROUGHNESS = roughness_value;
	SPECULAR = 0.12;
}
