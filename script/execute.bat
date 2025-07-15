chcp 65001
pushd %~dp0

    rem original
    python v1/update_route.py ../database/神奈川中央交通 ../work/busstops.json
    python v1/generate.py ../database/神奈川中央交通 True

    rem v1
    python v1/update_route.py ../database/kanachu/v1/database ../work/busstops.json
    python v1/generate.py ../database/kanachu/v1/database True

popd
