import title
import event
import icon
import os
import time
import PySimpleGUI as sg

colors = [
    "#9ADD1C",
    "#FFCA19",
    "#FF7FB4",
    "#55D1F0",
    "#8D9EFF"
]


def print_event(event):
    title = event['e']
    txt = ""
    for c in event['choices']:
        txt += f"\nΩ {c['n']}\n    "
        lines = c['t'].split('[br]')
        txt += '\n     '.join(lines)
    print(f"イベント：{title}\n{txt}")


def show_event_window(pos, event):
    left, top, width = pos
    title = event['e']
    layout = [
        [sg.Text(title, font=('Helvetica', 10, 'bold'))]
    ]
    line = 0
    for idx, c in enumerate(event['choices']):
        line += 1
        lines = c['t'].split('[br]')
        line += len(lines)
        mes = '        ' + '\n         '.join(lines)
        layout.append([sg.Text(
            "Ω",
            font=('Helvetica', 8, 'bold'),
            text_color=colors[idx % len(colors)],
            background_color='white'
        ), sg.Text(
            c['n'],
            font=('Helvetica', 8, 'bold'),
            text_color="#222222",
            background_color='white'
        )])
        layout.append([sg.Text(
            mes,
            font=('Helvetica', 8, 'bold'),
            text_color="#444444",
            background_color='white',
            pad=((10, 0), (0, 3))
        )])
    return sg.Window(
        'event window',
        layout,
        size=(400, 40 + 30 * line),
        location=(left + width, top),
        background_color='white',
        keep_on_top=True,
        auto_size_buttons=False,
        grab_anywhere=False,
        no_titlebar=True,
        return_keyboard_events=False,
        alpha_channel=0.8,
        use_default_focus=False,
        finalize=True
    )


pre_event = None
window = None
print('イベント：None')
while(True):
    e = None
    sleep = False
    if window is not None:
        window.read(timeout=10)
    pos = title.locate_window()
    if pos is not None:
        left, top, width = pos
        event_type = icon.detect_event_type(left, top ,width)
        if event_type is None:
            os.system('cls')
            print("not event scene")
            sleep = True
        else:
            txt = title.get_str(left, top, width)
            os.system('cls')
            print(f"window: (left,top,width)=({left},{top},{width}) ")
            print(f"ocr txt: {txt}")
            events = event.find_event(txt)
            if len(events) == 1:
                e = events[0]
            elif len(events) == 0:
                e = None
            else:
                name = icon.detect_name(left, top, width, event_type)
                if name is None:
                    e = None
                else:
                    e = event.filter_events(events, name)
    else:
        os.system('cls')
        print("window: None")
        sleep = True
    if e is None:
        if window is not None:
            window.close()
        window = None
    else:
        print_event(e)
        if pre_event is None or e['n'] != pre_event['n']:
            if window is not None:
                window.close()
            window = show_event_window(pos, e)
            window.read(timeout=500)
    pre_event = e
    if sleep:
        time.sleep(1)
