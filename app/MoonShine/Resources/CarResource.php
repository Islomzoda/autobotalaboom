<?php

declare(strict_types=1);

namespace App\MoonShine\Resources;

use App\Models\Brand;
use Illuminate\Database\Eloquent\Model;
use App\Models\Car;

use MoonShine\Fields\Relationships\BelongsTo;
use MoonShine\Fields\Relationships\HasOne;
use MoonShine\Fields\Text;
use MoonShine\Resources\ModelResource;
use MoonShine\Decorations\Block;
use MoonShine\Fields\ID;

class CarResource extends ModelResource
{
    protected string $model = Car::class;

    protected string $title = 'Машины';
    protected array $with = [
        'brand'
    ];

    public function fields(): array
    {
        return [
            Block::make(array(
                ID::make()->sortable(),
                Text::make('Название', 'name'),
                BelongsTo::make('Бренд', 'brand', fn($item) => $item->name)->searchable(),
                Text::make('Ссылка TJ', 'taj_url')->hideOnIndex(),
                Text::make('Ссылка RU', 'rus_url')->hideOnIndex(),
            )),
        ];
    }

    public function rules(Model $item): array
    {
        return [];
    }
}
