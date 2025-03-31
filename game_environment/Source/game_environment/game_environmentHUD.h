// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once 

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "game_environmentHUD.generated.h"

UCLASS()
class Agame_environmentHUD : public AHUD
{
	GENERATED_BODY()

public:
	Agame_environmentHUD();

	/** Primary draw call for the HUD */
	virtual void DrawHUD() override;

private:
	/** Crosshair asset pointer */
	class UTexture2D* CrosshairTex;

};

