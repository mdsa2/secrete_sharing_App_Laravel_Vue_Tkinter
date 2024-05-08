<?php

namespace App\Http\Controllers;

use App\Models\Share;
use Carbon\Carbon;
use Illuminate\Support\Facades\Session;
use Illuminate\Database\Eloquent\ModelNotFoundException;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Log;

use Tymon\JWTAuth\Facades\JWTAuth;


class AuthController extends Controller
{

    public function login(Request $request)
    {
        try {
            // Retrieve the user's credentials from the request
            $credentials = $request->only('id', 'password');

            Log::debug('Received credentials: ' . json_encode($credentials));

            // Retrieve the user by ID
            $user = Share::findOrFail($credentials['id']);

            // Check if the password matches
            if ($credentials['password'] == $user->y) {
                // Retrieve the current active login status for all users
                $activeLogins = Share::whereNotNull('last_login_at')->count();

                // Increment the count of active logins
                $activeLogins++;

                // Log debug message for active logins
                Log::debug('Active logins: ' . $activeLogins);

                // Update the last login time
                $user->update(['last_login_at' => Carbon::now()]);

                // Determine the authentication message based on active logins
                $message = $activeLogins == 1 ? 'First user authentication successful' : 'Second user authentication successful';

                // Generate JWT token
                $token = JWTAuth::fromUser($user);

                // Return token along with response
                return response()->json([
                    'message' => $message,
                    'token' => $token,
                    'active_login_status' => $activeLogins
                ]);
            } else {
                return response()->json(['message' => 'Invalid credentials'], 401);
            }
        } catch (ModelNotFoundException $e) {
            // User not found
            return response()->json(['message' => 'User not found'], 404);
        } catch (\Exception $e) {
            // Log any exceptions that occur during authentication
            Log::error('Authentication error: ' . $e->getMessage());
            return response()->json(['message' => 'An error occurred during authentication.'], 500);
        }
    }




}
