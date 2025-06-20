import os
import random
import sys
import time
import pygame as pg



WIDTH, HEIGHT = 1100, 650
DELTA = {  # 移動量辞書
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))




def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向、縦方向の画面内判定結果
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True  # 初期値：画面内
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate  # 横方向、縦方向の画面内判定結果を返す


def gameover(screen: pg.Surface) -> None:
    """
    こうかとんに爆弾が着弾した際にゲームオーバー画面を表示
    """
    black_img = pg.Surface((WIDTH, HEIGHT))  # 画面全体サイズ
    fonto = pg.font.Font(None, 70)  # 文字サイズ
    txt = fonto.render("Game Over", True, (255, 255, 255))  # 文章と文字色
    rct = txt.get_rect()  # 文字の表示範囲の取得
    rct.center = WIDTH/2, HEIGHT/2  # 取得した表示範囲の中心の設定
    pg.draw.rect(black_img, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))  # ブラックアウトの描画
    black_img.set_alpha(200)  # 透明度
    kk2_img = pg.image.load("fig/8.png")
    kk2_img = pg.transform.rotozoom(kk2_img, 0, 1.5)
    screen.blit(black_img, [0, 0])
    screen.blit(kk2_img, [300, HEIGHT/2-50])  # 左のこうかとんの表示位置
    screen.blit(kk2_img, [750, HEIGHT/2-50])  # 右のこうかとんの表示位置
    screen.blit(txt, rct)
    pg.display.update()  # 画面更新
    time.sleep(5)  # 5秒停止


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズの異なる爆弾Surfaceを要素としたリストと加速度リストを返す
    戻り値：爆弾Surfaceのリスト、対応する加速度リスト
    """
    bb_imgs = []  # 爆弾リスト
    bb_kasoku = [a for a in range(1, 11)]  # 加速度リスト
    for r in range(1, 11):  # 爆弾10段階
        bb_img = pg.Surface((20*r, 20*r))  # 空のSurfaceを作る（爆弾用）
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)  # 赤い円を描く
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return bb_imgs, bb_kasoku


def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    kk_img_base = pg.image.load("fig/3.png")
    kk_img_base = pg.transform.rotozoom(kk_img_base, 0, 0.9)

    kk_imgs = {
        (5, 0): pg.transform.rotozoom(kk_img_base, 0, 1.0),   # 右
        (-5, 0): pg.transform.rotozoom(kk_img_base, 0, 1.0),  # 左
        (0, -5): pg.transform.rotozoom(kk_img_base, 90, 1.0), # 上
        (0, 5): pg.transform.rotozoom(kk_img_base, -90, 1.0), # 下
        (5, -5): pg.transform.rotozoom(kk_img_base, 45, 1.0), # 右上
        (-5, -5): pg.transform.rotozoom(kk_img_base, 135, 1.0),# 左上
        (5, 5): pg.transform.rotozoom(kk_img_base, -45, 1.0), # 右下
        (-5, 5): pg.transform.rotozoom(kk_img_base, -135, 1.0),# 左下
        (0, 0): pg.transform.rotozoom(kk_img_base, 0, 0.9) # 停止
    }


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))  # 空のSurfaceを作る（爆弾用）
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い円を描く
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()  # 爆弾Rectを取得
    bb_rct.centerx = random.randint(0, WIDTH)  # 横座標用の変数
    bb_rct.centery = random.randint(0, HEIGHT) # 縦座標用の変数
    vx, vy = +5, +5  # 爆弾の移動速度


    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):  # こうかとんRectと爆弾Rectの衝突判定
            gameover(screen)
            return
        
        bb_imgs, bb_kasoku = init_bb_imgs() 
        avx = vx * bb_kasoku[min(tmr//500, 9)]
        avy = vy * bb_kasoku[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        vx == avx  # 加速した速さに置き換える
        vy == avy  # 加速した速さに置き換える

        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 移動をなかったことにする
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(avx, avy)  # 爆弾の移動
        yoko, tate =check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 爆弾の描画

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
