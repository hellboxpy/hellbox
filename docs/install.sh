#!/bin/bash

# Based on rustup: https://github.com/rust-lang/rustup/blob/cb3556eaf68504e62b4e65a308a14b3a65c0bf1f/rustup-init.sh

if [ -z "$HELL_RELEASE_ROOT" ]; then
    HELL_RELEASE_ROOT="https://github.com/hellboxpy/hell/releases/download"
fi

set -u

main() {
    get_architecture || return 1
    local _arch="$RETVAL"
    assert_nz "$_arch" "arch"

    local _version="v0.2.0"
    local _url="${HELL_RELEASE_ROOT}/${_version}/hell-${_arch}"

    local _dir
    _dir="$(mktemp -d 2>/dev/null || ensure mktemp -d -t hell)"
    local _file="${_dir}/hell"
    local _destination="$HOME/.hell/bin"

    printf '%s\n' 'info: downloading hell' 1>&2

    ensure mkdir -p "$_dir"
    ensure downloader "$_url" "$_file"
    ensure chmod u+x "$_file"
    ensure mkdir -p "$_destination"
    ensure mv "$_file" "$_destination/hell"
    ensure "$_destination/hell" _postinstall
    cat <<EOF
Ensure that you can run the CLI by adding ~/.hell/bin path to PATH:

  PATH=~/.hell/bin:\$PATH

EOF
}

get_bitness() {
    need_cmd head
    # Architecture detection without dependencies beyond coreutils.
    # ELF files start out "\x7fELF", and the following byte is
    #   0x01 for 32-bit and
    #   0x02 for 64-bit.
    # The printf builtin on some shells like dash only supports octal
    # escape sequences, so we use those.
    local _current_exe_head
    _current_exe_head=$(head -c 5 /proc/self/exe )
    if [ "$_current_exe_head" = "$(printf '\177ELF\001')" ]; then
        echo 32
    elif [ "$_current_exe_head" = "$(printf '\177ELF\002')" ]; then
        echo 64
    else
        panic "unknown platform bitness"
    fi
}

get_architecture() {
    local _ostype _cputype _arch
    _ostype="$(uname -s)"
    _cputype="$(uname -m)"

    if [ "$_ostype" = Linux ]; then
        if [ "$(uname -o)" = Android ]; then
            _ostype=Android
        fi
    fi

    if [ "$_ostype" = Darwin ] && [ "$_cputype" = i386 ]; then
        # Darwin `uname -m` lies
        if sysctl hw.optional.x86_64 | grep -q ': 1'; then
            _cputype=x86_64
        fi
    fi

    case "$_ostype" in

        Linux)
            _ostype=unknown-linux-gnu
            ;;

        Darwin)
            _ostype=apple-darwin
            ;;

        MINGW* | MSYS* | CYGWIN*)
            _ostype=pc-windows-gnu
            ;;

        *)
            panic "unrecognized OS type: $_ostype"
            ;;

    esac

    case "$_cputype" in

        aarch64 | arm64)
            _cputype=aarch64
            ;;

        x86_64 | x86-64 | x64 | amd64)
            _cputype=x86_64
            ;;

        *)
            panic "unknown CPU type: $_cputype"

    esac

    # Detect 64-bit linux with 32-bit userland for x86
    if [ "$_ostype" = unknown-linux-gnu ] && [ "$_cputype" = x86_64 ]; then
        if [ "$(get_bitness)" = "32" ]; then
            _cputype=i686
        fi
    fi

    # Detect 64-bit linux with 32-bit userland for powerpc
    if [ $_ostype = unknown-linux-gnu ] && [ $_cputype = powerpc64 ]; then
        if [ "$(get_bitness)" = "32" ]; then
            local _cputype=powerpc
        fi
    fi

    # Detect armv7 but without the CPU features Rust needs in that build,
    # and fall back to arm.
    # See https://github.com/rust-lang/hell.rs/issues/587.
    if [ "$_ostype" = "unknown-linux-gnueabihf" ] && [ "$_cputype" = armv7 ]; then
        if ensure grep '^Features' /proc/cpuinfo | grep -q -v neon; then
            # At least one processor does not have NEON.
            _cputype=arm
        fi
    fi

    _arch="${_cputype}-${_ostype}"

    RETVAL="$_arch"
}

say() {
    printf 'hell: %s\n' "$1"
}

panic() {
    say "$1" >&2
    exit 1
}

need_cmd() {
    if ! check_cmd "$1"; then
        panic "need '$1' (command not found)"
    fi
}

check_cmd() {
    command -v "$1" > /dev/null 2>&1
}

need_ok() {
    if [ $? -ne 0 ]; then panic "$1"; fi
}

assert_nz() {
    if [ -z "$1" ]; then panic "assert_nz $2"; fi
}

# Run a command that should never fail. If the command fails execution
# will immediately terminate with an error showing the failing
# command.
ensure() {
    "$@"
    need_ok "command failed: $*"
}

# This wraps curl or wget. Try curl first, if not installed,
# use wget instead.
downloader() {
    local _dld
    if check_cmd curl; then
        _dld=curl
    elif check_cmd wget; then
        _dld=wget
    else
        _dld='curl or wget' # to be used in error message of need_cmd
    fi

    if [ "$1" = --check ]; then
        need_cmd "$_dld"
    elif [ "$_dld" = curl ]; then
        curl -sSfL "$1" -o "$2"
    elif [ "$_dld" = wget ]; then
        wget "$1" -O "$2"
    else
        panic "Unknown downloader"   # should not reach here
    fi
}

main "$@" || exit 1
