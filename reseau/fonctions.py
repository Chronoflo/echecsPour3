from kivy.metrics import Metrics

def px_to_m(px):
    res = 0.0254 * px / Metrics.dpi
    return res

if __name__ == '__main__':
    print(px_to_m(100))
