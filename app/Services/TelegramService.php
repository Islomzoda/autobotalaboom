<?php

namespace App\Services;

use Telegram\Bot\Laravel\Facades\Telegram;

class TelegramService
{
    public function handle(Request $request)
    {
        $update = Telegram::commandsHandler(true);

        // Обработка команды /all
        if ($update->isType('command') && $update->getCommand() == 'all') {
            return $this->handleAllCommand($update);
        }

        // Добавьте обработчики для других команд, если необходимо

        return 'OK';
    }

    private function handleAllCommand($update)
    {
        $keyboard = [];

        // Здесь вы можете добавить логику для получения списка брендов из базы данных
        $brands = ['Brand1', 'Brand2', 'Brand3'];

        foreach ($brands as $brand) {
            $keyboard[] = [$brand];
        }

        $replyMarkup = [
            'keyboard' => $keyboard,
            'resize_keyboard' => true,
            'one_time_keyboard' => true,
        ];

        Telegram::sendMessage([
            'chat_id' => $update->getChat()['id'],
            'text' => 'Выберите бренд:',
            'reply_markup' => json_encode($replyMarkup),
        ]);

        return 'OK';
    }
}
