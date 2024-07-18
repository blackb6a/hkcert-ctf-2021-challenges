from nacl.bindings.crypto_secretstream import *

# extract from dynamic analysis after knowing whats going on
key = int("d5e5ab10e7c3e61b6e9820f4dece0ea0e0e78241cf4463ae523e496961cdbfd7", 16).to_bytes(32, "big")
c = int("cb4c49906a7f7b7359e7662a29d84cf2f11d7e70bceb32d81b9131bd35d2f0f69319bffb09835f0777e0b18cacb929941db89b7aaa6dccc77747e7b02431ed1e863beb577d346710b5eda95cf86ca4e84a", 16).to_bytes(81, "big")

hdr = c[:crypto_secretstream_xchacha20poly1305_HEADERBYTES]
state = crypto_secretstream_xchacha20poly1305_state()
crypto_secretstream_xchacha20poly1305_init_pull(state, hdr, key)
hdr = c[:crypto_secretstream_xchacha20poly1305_HEADERBYTES]
state = crypto_secretstream_xchacha20poly1305_state()
crypto_secretstream_xchacha20poly1305_init_pull(state, hdr, key)
frame = c[24:]
chunk, tag = crypto_secretstream_xchacha20poly1305_pull(state, frame)
print(chunk)
# b'hkcert21{ju5t_An0th3r_br0k3n_r4nD0mN3s3}'