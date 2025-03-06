// Copyright Epic Games, Inc. All Rights Reserved.

#include "game_environmentGameMode.h"
#include "game_environmentHUD.h"
#include "game_environmentCharacter.h"
#include "UObject/ConstructorHelpers.h"

Agame_environmentGameMode::Agame_environmentGameMode()
	: Super()
{
	// set default pawn class to our Blueprinted character
	static ConstructorHelpers::FClassFinder<APawn> PlayerPawnClassFinder(TEXT("/Game/FirstPersonCPP/Blueprints/FirstPersonCharacter"));
	DefaultPawnClass = PlayerPawnClassFinder.Class;

	// use our custom HUD class
	HUDClass = Agame_environmentHUD::StaticClass();
}
